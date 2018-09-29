#基于Token及用户权限的Flask-Restful的BaaS API
1. 以Token为认证
2. 拥有用户角色权限管理

#
默认登陆用户名为admin/ad
目前功能可以自动扫描脚本，自动配置参数

# 20180921
修改使用config.py
可配置后台运行任务
统一日志设置
修改部分db.view视图

# 20180928
后台任务，发送email
配置gunicorn
加入Manage
加入shell
重建数据库

# 20180929
utf8问题
job目录不能cython

    
    python manage.py shell
    
    db.drop_all()
    db.create_all()
    user_test1 = User(username=u"test1", password=u"test1")
    user_test2 = User(username=u"test2", password=u"test2")
    user_string = User(username=u"string", password=u"string")
    user_admin = User(username=u"admin", password=u"ad")
    role_admin = Role(name=u"admin", description=u"admin")
    
    shell1 = ShellFile(name=u"bp.sh", path=u"bp.sh")
    shell2 = ShellFile(name=u"before.sh", path=u"before.sh")
    shell3 = ShellFile(name=u"after.sh", path=u"after.sh")
    
    aps_jobid='[baas.jobs.jobs:job1-1]'
    job1 = ApsJobs(aps_jobid=aps_jobid, aps_func='baas.jobs.jobs:job1', aps_args='888 888',
                   aps_tirgger='cron', aps_cron='*/2 * * * * * *')
    aps_jobid = '[baas.jobs.jobs:shell_job]'
    job2 = ApsJobs(aps_jobid=aps_jobid, aps_func='baas.jobs.jobs:shell_job', aps_args='bp.bat 999 999',
                   aps_tirgger='cron', aps_cron='*/2 * * * * * *')
    
    session = db.create_session({})()
    session.add(user_test1)
    session.add(user_test2)
    session.add(user_string)
    session.add(user_admin)

    # https://stackoverflow.com/questions/45044926/db-model-vs-db-table-in-flask-sqlalchemy
    user_admin.roles.append(role_admin)
    session.add(role_admin)
    session.add(job1)
    session.add(job2)
    session.add(shell1)
    session.add(shell2)
    session.add(shell3)
    session.commit()
    
    exit()
