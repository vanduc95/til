import subprocess

p1 = subprocess.Popen(['sudo', 'find', '/var/log/', '-printf', '%T+ %p\n'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['sort', '-nr'], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()
p3 = subprocess.Popen(['head', '-n', '1'], stdin=p2.stdout, stdout=subprocess.PIPE)
p2.stdout.close()

# output = p3.communicate()[0]
# print(output)
# a = output.decode

print('# HELP latest_file_update_in_directory')
print('# TYPE latest_file_update_in_directory gauge')

print('latest_file_update_in_directory{directory="%s",file="%s"} %f' % ('/var/log/', '/var/log/abc.log', 1.559727986e+09))
