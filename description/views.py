from django.shortcuts import render, redirect
import paramiko
import environ
import re
import netmiko
import json
from netmiko import ConnectHandler






env = environ.Env()

hostname = env('HOST_NAME')
username = env('USER_NAME')
password = env('PASSWORD')




def show_description(request):
    
    context = {}
    
    if request.method == 'POST':
        try:
            # Initialize SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the device
            ssh.connect(hostname=hostname, username=username, password=password)
            
            # Execute the command to show interfaces
            command = env('SHOW_INTERFACE_DESCRIPTION')
            
            stdin, stdout, stderr = ssh.exec_command(command)
            
            # Print the command output
            output = stdout.read().decode('utf-8')
            
            # lines = output.splitlines()
            
            # data = []
            # for line in lines:
            #     columns = re.split(r'\s+', line)
                
            #     if len(columns) > 1:
            #         data.append(columns)
            
            # context = {
            #     "data":data
            # }
            
            context = {
                "data":output
            }

            print(type(output))

            
            # Close the connection
            ssh.close()

            return render(request, 'description/get-description.html', context)

        except paramiko.AuthenticationException:
            print("Authentication failed. Please check your credentials.")
        except paramiko.SSHException as ssh_exception:
            print(f"Error connecting to the device: {ssh_exception}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    return render(request, 'description/get-description.html', context)