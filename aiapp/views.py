from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import json
#models
from .models import UserInteractionCollection
from .models import Interaction
from .models import ImageUpload
from user.models import User
# serilaizer
from .serializers import UserInteractionCollectionSerializer
from .serializers import InteractionSerializer
#utility
from .google_bard import *
from Bard_ecosystem_BE.utils.utility import encrypt_token,is_user_authenticated
#from Bard_ecosystem_BE.utils.aiapp_utility import generate_title
import cloudinary.uploader
from cloudinary.uploader import upload_image
# -------- get --------

class UserlistColectionsView(APIView):
    def get(self, request):
        auth_result, is_authenticated = is_user_authenticated(request)
        if is_authenticated:
            user_id=auth_result['user_token_data']['user_id']
            print("user_id : ",user_id)
            collections = UserInteractionCollection.objects.all().order_by('-created_at')
            serializer = UserInteractionCollectionSerializer(collections,many=True)
            return Response({'collections':serializer.data}, status=status.HTTP_200_OK)
        else:
            # Handle unauthenticated requests
            return Response({'message':auth_result['message'] }, status=auth_result['status'])
        

class UserlistInteractionsView(APIView):
    def get(self, request,collection_id):
        auth_result, is_authenticated = is_user_authenticated(request)
        if is_authenticated:
            user_id=auth_result['user_token_data']['user_id']
            print("user_id : ",user_id)
            interactions = Interaction.objects.filter(interaction_collection=collection_id).order_by('created_at')
            print(interactions)
            if interactions:
                serializer = InteractionSerializer(interactions,many=True)
                return Response({'interactions':serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"Error": "No such Collection exists"}, status=status.HTTP_404_NOT_FOUND)
                
                
        else:
            # Handle unauthenticated requests
            return Response({'message':auth_result['message'] }, status=auth_result['status'])
        
        
# --------- post ----------    
        
class StartInteractionView(APIView):
    def post(self, request):
        auth_result, is_authenticated = is_user_authenticated(request)
        if is_authenticated:
            user_id=auth_result['user_token_data']['user_id']
            user_chat = request.data.get('user_chat').replace('"', '')
            image = request.FILES.get('image')
            # Get the response including the provided image
            response_data = get_response(user_chat, image=image)
            response_chat = response_data['response']
            #generated_title = generate_title(user_chat)
            generated_title = generate_title_using_bard(user_chat)['response']
            interaction_type = request.data.get('interaction_type')
            title = request.data.get('title')
            if not user_chat:
                return Response({'error': 'Missing user_chat field'}, status=status.HTTP_400_BAD_REQUEST)
            else: 
                try:
                    user=User.objects.get(id=user_id)
                    # Create a new UserInteractionCollection object.
                    collection = UserInteractionCollection.objects.create(
                        title=generated_title, 
                        creator=user
                    )
                    # Create a new Interaction object with provided data.
                    try:
                        interaction = Interaction.objects.create(
                            user_chat = user_chat, 
                            response_chat=response_chat,
                            interaction_collection=collection,
                            #interaction_type=interaction_type, 
                        )
                    
                        # Serialize the collection and interaction for response.
                        collection_serializer = UserInteractionCollectionSerializer(collection)
                        interaction_serializer = InteractionSerializer(interaction)

                        return Response({
                            'collection': collection_serializer.data,
                            'interaction': interaction_serializer.data
                        }, status=status.HTTP_201_CREATED)
                    except Exception as E:
                        return Response({"Message":"unexpected issue in model serializer."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except UserInteractionCollection.DoesNotExist:
                    return Response({"Message":"this interactions collection not found"},status=status.HTTP_404_NOT_FOUND)
        else:
            # Handle unauthenticated requests
            return Response({'message':auth_result['message'] }, status=auth_result['status'])
       
class StartInteractionWithCollectionIdView(APIView):
    def post(self, request,collection_id):
        auth_result, is_authenticated = is_user_authenticated(request)
        if is_authenticated:
            user_id=auth_result['user_token_data']['user_id']
            user_chat = request.data.get('user_chat').replace('"', '')
            image = request.FILES['image'].read()
            response_data =get_response(user_chat, image=image)
            response_chat = response_data['response']
            interaction_type = request.data.get('interaction_type')
                
            if not user_chat:
                return Response({'error': 'Missing user_chat field'}, status=status.HTTP_400_BAD_REQUEST)
            else: 
                try:
                    collection = UserInteractionCollection.objects.get(pk=collection_id)
                except UserInteractionCollection.DoesNotExist:
                    return Response({"Message":"this interactions collection not found"},status=status.HTTP_404_NOT_FOUND)
                if collection:
                    try:
                        #if image:
                        #    # Upload image to Cloudinary
                            
                        #    # Process image here if needed
                        #    image_bytes = image.read()
                        #    # Open the image using PIL
                        #    image_pil = PIL.Image.open(BytesIO(image_bytes))
                        #    print(image_pil)
                            
                        #    upload_result = upload_image(image_pil)
                        #    print(upload_result)
                        #    image_url = upload_result['url']

                        #    # Create interaction with image URL
                        #    interaction = Interaction.objects.create(
                        #        user_chat=user_chat,
                        #        response_chat=response_chat,
                        #        interaction_collection=collection,
                        #        image=image_url,
                        #        interaction_type=interaction_type,
                        #    )
                        #else:
                        #    # Create interaction without image
                        #    interaction = Interaction.objects.create(
                        #        user_chat=user_chat,
                        #        response_chat=response_chat,
                        #        interaction_collection=collection,
                        #        interaction_type=interaction_type,
                        #    )
                        
                        # Open the image using PIL
                        image_pil = PIL.Image.open(BytesIO(image))
                        imageuploaded = cloudinary.uploader.upload(image_pil)
                        interaction = Interaction.objects.create(
                            user_chat=user_chat,
                            response_chat=response_chat,
                            interaction_collection=collection,
                        )
                        interaction_serializer = InteractionSerializer(interaction)
                        return Response({
                            'interaction': interaction_serializer.data
                        }, status=status.HTTP_201_CREATED)
                        
                    except UserInteractionCollection.DoesNotExist:
                        return Response({"Message":"failed to create new interaction"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"Error": "No such Collection exists"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Handle unauthenticated requests
            return Response({'message':auth_result['message'] }, status=auth_result['status'])
       
       
#from django.shortcuts import render, HttpResponseRedirect
#from django.core.exceptions import ValidationError
#from rest_framework.views import APIView
#from rest_framework.parsers import MultiPartParser, FormParser
#from rest_framework.response import Response
#from rest_framework import status
#import cloudinary.uploader

#class ImageUploadView(APIView):
#    #parser_classes = [MultiPartParser, FormParser]

#    def post(self, request):
#        try:
#            # Access the uploaded image file from the request
#            image_file = request.FILES['image']

#            # Upload the image to Cloudinary using your credentials
#            upload_result = cloudinary.uploader.upload(image_file)
#            image_url = upload_result["url"]

#            # Create a new ImageUpload model instance with the URL
#            image_upload = ImageUpload(image_url=image_url)
#            image_upload.save()

#            return Response({'message': 'Image uploaded successfully!', 'url': image_url}, status=status.HTTP_201_CREATED)

#        except (KeyError, ValidationError):
#            return HttpResponseRedirect('Invalid request data or image format')
#        except cloudinary.exceptions.Error as e:
#            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#class generatetitle(APIView):
#    def post(self, request):
#       generate_title("hello nebula can you help me please?")
    


    


#def audio_conversion(self, request): 
#    audio_file = request.data.get('audio', None) 
#    user = request.data.get('user_id',None) 
#    chat_type = request.data.get('chat_type', None) 
#    if chat_type =='audio' : 
#        try: 
#            audio_content = audio_file.read() 
#            audio_segment = AudioSegment.from_file( io.BytesIO(audio_content), frame_rate=44100, channels=2, sample_width=2 ) 
#            modified_audio_content = audio_segment.export( format="mp3").read() 
#            file_name = audio_file._name 
#            modified_audio_file = ContentFile( modified_audio_content, name=f'{file_name}.mp3') 
#            data = request.data.copy() 
#            data['audio'] = modified_audio_file 
#            serializer = ChatHistorySerializer(data=data) 
#            if serializer.is_valid(): 
#                chat_history = serializer.save()
#                modified_audio_content = None 
#                return chat_history 
#        except Exception as E: 
#            return Response(str(E), status=400) 
#    else: return Response({"error": "No audio file found"}, status=400)




#def create_user_interaction(request):
#    if request.method == 'POST':  # Corrected to uppercase 'POST'
#        interaction = json.loads(request.body.decode('utf-8'))
#        serialized_interactions = UserInteractionCollectionSerializer(data=interaction)
#        if serialized_interactions.is_valid():
#            print ("interaction row created successfully")
#            serialized_interactions.save()
#            return JsonResponse({'message': 'Successfully created new interaction row'}, status=201)
#        else:
#            return JsonResponse(serialized_interactions.errors, status=400)
#    else:
#        return JsonResponse({'message': 'Method not allowed'}, status=405)
    
#@csrf_exempt
#def get__all_users_interaction(request):
#    if request.method =='GET':
#        interactions = UserInteractionCollection.objects.all().order_by('timestamp')
#        serialized_interactions = UserInteractionCollectionSerializer(data=interactions,many=True)
#        return JsonResponse(data=serialized_interactions, safe=False, status=200)
#    else:
#        return JsonResponse({'message': 'Method not allowed'}, status=405)
    
#@csrf_exempt       
#def get_specific_user_interactions(request,user_id):
#    try:
#        user = UserInteractionCollection.objects.get(pk=user_id)
#    except UserInteractionCollection.DoesNotExist:
#        return HttpResponse({'message' : 'User Interactions does not exist'},status=404)
    
#    if request.method =='GET':
#        user_interactions = UserInteractionCollection.objects.get(user_id).order_by('timestamp')
#        serialized_interactions = UserInteractionCollectionSerializer(data=user_interactions,many=True)
#        return JsonResponse(data=serialized_interactions, safe=False, status=200)
#    else:
#        return JsonResponse({'message': 'Method not allowed'}, status=405)
   
        
        
#@csrf_exempt
#def update_user_interaction(request,iteraction_id):
#	try:
#		user_interaction = UserInteractionCollection.objects.get(pk=iteraction_id)
#	except UserInteractionCollection.DoesNotExist:
#		return HttpResponse({"Message":"User Interaction Does Not Exists"},status=404) 

#	if request.method == 'PUT':
#		data=json.loads(request.body.decode('utf-8'))
#		serializer = UserInteractionCollectionSerializer(data=user_interaction)
#		if serializer.is_valid():
#			print ("interaction row created successfully")
#			serializer.save()
#			return JsonResponse({'message': 'Successfully update interaction row'}, status=201)
#		else:
#			return JsonResponse(serializer.errors, status=400)
#	else:
#		return JsonResponse({'message': 'Method not allowed'}, status=405)