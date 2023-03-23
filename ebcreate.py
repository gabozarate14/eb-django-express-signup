env = []
with open('env.txt','r') as fd:
    for l in fd.readlines():
        (k,v)=l.split('=',1)
        k = k.upper().strip()
        v = v.strip()
        env.append(f'{k}={v}')
        print(f'export {k}={v}')
print ('eb create -ip LabInstanceProfile --service-role LabRole  --elb-type application --envvars "%s"'%','.join(env))