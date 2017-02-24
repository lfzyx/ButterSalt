import jenkins

server = jenkins.Jenkins('http://192.168.1.72:8080', username='lfzyx', password='ac2365e7cd8ec7cb994b4547ead537da')


jobs = server.get_jobs(view_name='mz')
views = server.get_views()
cout = server.jobs_count()
print(jobs)
print(views)
print(cout)