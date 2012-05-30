from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, RequestContext
from session_manager.models import Session
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import paramiko

# Python decorator requiring using accessing view to be logged in
# If used is not logged in they get redirected to /login/
@login_required(login_url='/login/')
def manage_view(request, primary_key):
    obj = get_object_or_404(Session,pk=primary_key)

    # While the user is logged in, we still need to check that they own the object they requested
    if obj.owner != request.user:
        return HttpResponseForbidden("User not authorized.")

    data_dict = {'obj': obj}

    # If the user submitted a command, run it over an SSH session
    if request.method == "POST":
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(obj.hostname, username=obj.username, password=obj.password)

        command = request.POST.get('command')
        if command:
            if command[0:3] == "cd ":
                obj.cwd = command[3:]
                print "cwd: " + command[3:]
                obj.save()
            # Paramiko won't preserve the current working directory if we 'cd' into it with a
            # separate command, it has to be all done in the same command
            stdin, stdout, stderr = ssh.exec_command("cd " + obj.cwd + "; " + command)
            data_dict['stdout'] = stdout.read()
        else:
            data_dict['stdout'] = "ERROR: Please specify a command."

    return render_to_response('manage.html', data_dict, context_instance=RequestContext(request))


