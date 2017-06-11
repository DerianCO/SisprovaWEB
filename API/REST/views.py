import datetime
from django.shortcuts import render, get_object_or_404

from django.http import JsonResponse

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from API.Centros.models import Sede
from API.Elementos.models import Elemento
from API.Reportes.models import Reporte,ElementosReporte
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User


class ReporteAPI(APIView):

    #Peticion por post para generar un nuevo registro de ingreso o salida.

    def post(self,request,format=None):

        #Se valida que el codigo de la sede sea correcto, de lo contrario se envia un error 404
        sede = get_object_or_404(Sede, pk=request.data['idSede'])

        #Se valida que exista un usuario acorde al numero de identificacion recibido.
        if User.objects.filter(username=request.data['idPropietario']).exists():

            #Si el usuario existe, lo almacenamos en una variable llamada propietario.
            propietario = get_object_or_404(User,username=request.data['idPropietario'])

            #Se valida que se haya enviado el atributo idElemento en la peticion.
            if request.POST.get('idElemento'):

                #Se valida que exista un elemento acorde al atributo idELemento enviado en la peticion.
                if Elemento.objects.filter(pk=request.data['idElemento']).exists():

                    #Si el elemento existe, lo almacenamos en la variable elemento, de lo contrario retornamos un error 404
                    elemento = get_object_or_404(Elemento,pk=request.data['idElemento'])

                    #Se valida que exista un elemento, acorde al idElemento y que tenga un propietario acorde al idPropietario
                    if Elemento.objects.filter(pk=request.data['idElemento'],pro_ele=propietario).exists():

                        #Se valida si existe algun reporte con ese propietario que no tenga hora de salida.
                        if Reporte.objects.filter(pro_rep=propietario,fecha_hora_sal=None).exists():

                            #Si existe, el reporte sera almacenado en la variable reporte, de lo contrario retornamos error 404
                            reporte = get_object_or_404(Reporte,sede_rep=sede,fecha_hora_sal=None,pro_rep=propietario)

                            #Se valida si existen elementos del reporte, acorde a el reporte, el codigo del elemento, y a su estatus.
                            if ElementosReporte.objects.filter(reporte=reporte,elemento__cod_ele=request.data['idElemento'],status=True):

                                #En caso de existir el elemento del reporte, este sera almacenado en una variable elemento, de lo contrario retornara error 404
                                elemento = get_object_or_404(ElementosReporte,reporte=reporte,elemento__cod_ele=request.data['idElemento'],status=True)

                                #Se modifica el estado del elemento
                                elemento.status = False

                                #Se genera la actualizacion del registro
                                elemento.save()

                                if ElementosReporte.objects.filter(reporte=reporte,status=True).exists():
                                    return JsonResponse({'error':True,'message':'La persona esta saliendo sin los dispositivos con los que entro'})
                                else:
                                    reporte.fecha_hora_sal = datetime.datetime.now()

                                    reporte.save()

                                    return JsonResponse({'error':False,'message':'Salida exitosa'})

                            elif ElementosReporte.objects.filter(reporte=reporte,elemento__cod_ele=request.data['idElemento']).exists() == False:

                                if Elemento.objects.filter(pk=request.data['idElemento']).exists():
                                    #Se genera un nuevo registro de Elemento en el reporte
                                    new_elemento = ElementosReporte()

                                    #Se añade el reporte
                                    new_elemento.reporte = reporte

                                    #Se añade elemento
                                    new_elemento.elemento = Elemento.objects.get(pk=request.data['idElemento'])

                                    #Se almacena el nuevo registro de Elemento del reporte
                                    new_elemento.save()

                                    #Se retorna informacion en formato JSON, especificando si ocurrio un error y el mensaje.
                                    return JsonResponse({'error':False,'message':'Entrada exitosa'})

                                else:
                                    return JsonResponse({'error':True,'message':'No existe un elemento acorde a el ID'})

                        else:

                            if ElementosReporte.objects.filter(elemento__cod_ele=request.data['idElemento'],status=True).exists():
                                return JsonResponse({'error':True,'message':'Este dispositivo ya se encuentra dentro.'})
                            else:
                                #Se genera un nuevo reporte
                                reporte = Reporte()

                                #Se añade la fecha y hora de ingreso al reporte
                                reporte.fecha_hora_ing = datetime.datetime.now()

                                #Se añade el propietario al reporte
                                reporte.pro_rep = propietario

                                #Se añade la sede al reporte
                                reporte.sede_rep = sede

                                #Se almacena el registro del nuevo reporte
                                reporte.save()

                                #Se genera un nuevo registro de Elemento en el reporte
                                new_elemento = ElementosReporte()

                                #Se añade el reporte
                                new_elemento.reporte = reporte

                                #Se añade elemento
                                new_elemento.elemento = Elemento.objects.get(pk=request.data['idElemento'])

                                #Se almacena el nuevo registro de Elemento del reporte
                                new_elemento.save()

                                #Se retorna informacion en formato JSON, especificando si ocurrio un error y el mensaje.
                                return JsonResponse({'error':False,'message':'Entrada exitosa'})
                    else:
                        #Se retorna informacion en formato JSON, especificando si ocurrio un error y el mensaje.
                        return JsonResponse({'error':True,'message':'No es propietario del elemento'})
                else:
                    #Se retorna informacion en formato JSON, especificando si ocurrio un error y el mensaje.
                    return JsonResponse({'error':True,'message':'No ningun elemento acorde al ID'})
            else:
                #Se valida si existe un reporte con la informacion del propietario y sin hora de salida
                if Reporte.objects.filter(pro_rep=propietario,fecha_hora_sal=None).exists():

                    #En caso de existir el reporte, este se almacenara en una variable reporte, de lo contrario se retornara un error 404
                    reporte = get_object_or_404(Reporte,sede_rep=sede,fecha_hora_sal=None,pro_rep=propietario)

                    if ElementosReporte.objects.filter(reporte=reporte).exists():

                        return JsonResponse({'error':True,'message':'La persona esta saliendo sin el dispositivo que entro.'})
                    else:
                        #Se añade la hora de salida al reporte
                        reporte.fecha_hora_sal = datetime.datetime.now()

                        #Se genera la actualizacion del reporte
                        reporte.save()

                        #Se retorna informacion en formato JSON, especificando si ocurrio un error y el mensaje.
                        return JsonResponse({'error':False,'message':'Salida exitosa'})
                else:
                    #Se genera un nuevo reporte
                    reporte = Reporte()

                    #Se añade la fecha y hora de ingreso al reporte
                    reporte.fecha_hora_ing = datetime.datetime.now()

                    #Se añade el propietario al reporte
                    reporte.pro_rep = propietario

                    #Se añade la sede al reporte
                    reporte.sede_rep = sede

                    #Se almacena el registro del nuevo reporte
                    reporte.save()

                    #Se retorna informacion en formato JSON, especificando si ocurrio un error y el mensaje.
                    return JsonResponse({'error':False,'message':'Entrada exitosa'})
        else:
            #Se retorna informacion en formato JSON, especificando si ocurrio un error y el mensaje.
            return JsonResponse({'error':True,'message':'No existe ningun usuario con esta identificacion'})

reporte = ReporteAPI.as_view()
