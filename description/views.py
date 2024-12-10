from django.shortcuts import render, redirect
import paramiko
import environ
import re
import netmiko
import json
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException
from ntc_templates.parse import parse_output
from django.http import HttpResponse
import os



env = environ.Env()

device_type = env('DEVICE_TYPE')
hostname = env('HOST_NAME')
username = env('USER_NAME')
password = env('PASSWORD')




def check_env_variable(request):
    net_textfsm = os.environ.get('NET_TEXTFSM', 'Not set')
    return HttpResponse(f'NET_TEXTFSM: {net_textfsm}')



def show_description(request):
    
    context = {}
    
    if request.method == 'POST':
        try:
            # Define the device connection details
            device = {
                'device_type':device_type, # Cisco router or switch version
                'host':hostname,       
                'username':username, 
                'password':password,
            }

            net_connect = ConnectHandler(**device)
            
            if "interface_description" in request.POST:
                button_name = "interface_description"
                command = env(str('SHOW_INTERFACE_DESCRIPTION'))
                
            elif "interface_brief" in request.POST:
                button_name = "interface_brief"
                command = env(str('SHOW_INTERFACE_BRIEF'))
                
            elif "device_version" in request.POST:
                button_name = "device_version"
                command = env(str('SHOW_VERSION'))
                
            elif "ip_interface" in request.POST:
                button_name = "ip_interface"
                command = env(str('SHOW_IP_INTERFACE'))
                
            elif "policy_map_details" in request.POST:
                button_name = "policy_map_details"
                # command = env(str('SHOW_RUN_POLICY_MAP'))
                command = "show run policy-map"

            elif "policy_map_names" in request.POST:
                button_name = "policy_map_names"
                command = env(str('SHOW_RUN_POLICY_MAP_NAME'))
                
            elif "running_configuration" in request.POST:
                button_name = "running_configuration"
                command = env(str('SHOW_RUN'))
                
            elif "ip_route" in request.POST:
                button_name = "ip_route"
                command = env(str('SHOW_IP_ROUTE'))
                
            elif "all_interface" in request.POST:
                button_name = "all_interface"
                command = env(str('SHOW_INTERFACES'))
                
            elif "process_cpu" in request.POST:
                button_name = "process_cpu"
                command = env(str('SHOW_PROCESS_CPU'))
            
            
            command_output = net_connect.send_command(command, use_genie==True)

            # print(command_output)
            
            net_connect.disconnect()
            context = {
                "data":command_output,
                "clicked_button_name":button_name
            }

            return render(request, 'description/get-description.html', context)
        
        except NetmikoTimeoutException:
            print("Connection timed out.")
        except NetmikoAuthenticationException:
            print("Authentication failed.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    return render(request, 'description/get-description.html', context)