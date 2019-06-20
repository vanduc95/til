import subprocess
process = subprocess.Popen(['echo', '"Hello stdout"'], stdout=subprocess.PIPE)
stdout = process.communicate()[0]
print('STDOUT:{}'.format(stdout))

output = process.stdout.readline()
print(output)