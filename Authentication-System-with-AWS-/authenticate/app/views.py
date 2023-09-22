from django.shortcuts import render
import requests
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
rekognition = boto3.client('rekognition', region_name='ap-south-1')
client = boto3.client('cognito-idp', region_name='ap-south-1')
user_pool_id = 'ap-south-1_sH4Elv9Tx'
def login(request):
    if request.method == 'POST':
        # Get the uploaded image
        uploaded_image = request.FILES['image']
        mail = request.POST['email']
        print(mail)
        # Connect to S3 and upload the image
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_S3_REGION_NAME)

        try:
            s3.upload_fileobj(uploaded_image, settings.AWS_S3_BUCKET_NAME, uploaded_image.name)
            return HttpResponseRedirect('/success/')
        except ClientError as e:
            print(e)
            return render(request, 'error.html', {'error': e})

    else:
        return render(request, 'login.html')


def success(request):
    return render(request,'success.html')

def error(request):
    return render(request,'error.html')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        uploaded_image = request.FILES['image']

        if(password!=confirm_password):
            error = "Password doesnt match"
            return render(request, 'register.html', {'error': error})
        else:
            try:
                response = client.sign_up(
                        ClientId='4qj5qpn8pt23v3efk9hsrosg8c',
                        Username=email,
                        Password=password,
                        UserAttributes=[
                            {
                                'Name': 'email',
                                'Value': email
                            }
                        ]
                    )
            except client.exceptions.UsernameExistsException:
                error = "Email already registered"
                return render(request, 'register.html', {'error': error})
        object_key = f"{email}.jpg"
        
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                            region_name=settings.AWS_S3_REGION_NAME)


        # add image in s3 bucket 
        print("add image in s3 bucket ")
        try:
            s3.upload_fileobj(uploaded_image, settings.AWS_S3_BUCKET_NAME, object_key)
            
        except ClientError as e:
        
            return render(request, 'error.html', {'error': e})

        
    
        msg = "Registration Successful"
        return render(request,'success.html',{'msg':msg})

    else:
        return render(request,'register.html')
