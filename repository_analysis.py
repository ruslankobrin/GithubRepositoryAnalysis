import requests
from datetime import datetime, timedelta

## test data
## owner: octocat
## rep: Hello-World


def get_req(req, owner, repos, since=None, until=None, state=None, branch='master'):

    if req == 'issues':
        params = dict(since=since, until=until, state=state)
    else:
        params = dict(since=since, until=until, state=state, branch=branch)

    sum_resp = []
    i = 1

    while True:
        response = requests.get(
            'https://api.github.com/repos/{}/{}/{}?per_page=100&page={}'.format(owner, repos, req, i),
            params=params)
        print(response.status_code)
        if response.status_code == 403:
            print('API rate limit exceeded!')
            return
        elif response.status_code == 404:
            print('Введены некорректные данные!')
            return

        resp = response.json()
        if not resp:
            break

        sum_resp += resp
        i += 1

    return sum_resp


def input_params():

    print('Введите логин владельца репозитория:')
    owner = input()

    print('Введите имя репозитория:')
    repos = input()

    return owner, repos


def input_branch():
    print('Введите название ветки:')
    branch = input()
    if not branch:
        branch = 'master'

    return branch


def input_date_params():
    print('Введите начальное время(2018-04-14)')
    since = input()

    try:
        since = datetime.strptime(since, '%Y-%m-%d')
    except ValueError as e:
        since = None

    print('Введите конечное время(2018-04-14)')
    until = input()
    try:
        until = datetime.strptime(until, '%Y-%m-%d')
    except ValueError as e:
        until = None

    return since, until


###########################################
#############commits#######################
###########################################

def count_author_commits(owner, repos):

    dict = {}
    branch = input_branch()
    since, until = input_date_params()

    print('Самые активные участники:')

    for element in get_req('commits', owner, repos, since=since, until=until, branch=branch):
        try:
            value = element['commit']['author']['email']
            dict.update({value: int(dict.get(value)) + 1})
        except TypeError as e:
            dict.update({value: 1})

    return dict


def sort_reverse_author_commits(owner, repos):

    list_author_commits = list(count_author_commits(owner, repos).items())
    list_author_commits.sort(key=lambda i: i[1], reverse=True)

    return list_author_commits


def print_list_author_commits(owner, repos):

    for i in enumerate(sort_reverse_author_commits(owner, repos)):
        print(i[1])
        if i[0] == 30:
            break


###########################################
#############pull requests#################
###########################################

def count_open_pull_requests(owner, repos):

    branch = input_branch()
    since, until = input_date_params()
    print('Количество открытых pull requests на заданном периоде времени:')

    return len(get_req('pulls', owner, repos, since, until, state='open', branch=branch))


def count_closed_pull_requests(owner, repos):

    branch = input_branch()
    since, until = input_date_params()
    print('Количество закрытых pull requests на заданном периоде времени:')

    return len(get_req('pulls', owner, repos, since, until, state='closed', branch=branch))


def count_old_pull_requests(owner, repos):

    branch = input_branch()
    since, until = input_date_params()
    print('Количество “старых” pull requests на заданном периоде времени:')
    counter = 0
    old_zone = datetime.now() - timedelta(30)
    for element in get_req('pulls', owner, repos, since, until, state='open', branch=branch):
        created = datetime.strptime(element['created_at'], '%Y-%m-%dT%H:%M:%SZ')

        if created < old_zone:
            counter += 1

    return counter


###########################################
###################issues##################
###########################################

def count_open_issues(owner, repos):

    since, until = input_date_params()
    print('Количество открытых issues на заданном периоде времени:')

    return len(get_req('issues', owner, repos, since, until, state='open'))


def count_closed_issues(owner, repos):

    since, until = input_date_params()
    print('Количество закрытых issues на заданном периоде времению:')

    return len(get_req('issues', owner, repos, since, until, state='closed'))


def count_old_issues(owner, repos):

    since, until = input_date_params()
    print('Количество “старых” issues на заданном периоде времению:')
    counter = 0
    old_zone = datetime.now() - timedelta(14)
    for element in get_req('issues', owner, repos, since, until, state='open'):
        created = datetime.strptime(element['created_at'], '%Y-%m-%dT%H:%M:%SZ')

        if created < old_zone:
            counter += 1

    return counter


def main():

    owner, repos = input_params()
    try:
        print('\nСамые активные участники:\n'.upper())
        print_list_author_commits(owner, repos)
        print('\nКоличество открытых pull requests на заданном периоде времени:\n'.upper())
        print(count_open_pull_requests(owner, repos))
        print('\nКоличество закрытых pull requests на заданном периоде времени:\n'.upper())
        print(count_closed_pull_requests(owner, repos))
        print('\nКоличество “старых” pull requests на заданном периоде времени:\n'.upper())
        print(count_old_pull_requests(owner, repos))
        print('\nКоличество открытых issues на заданном периоде времени:\n'.upper())
        print(count_open_issues(owner, repos))
        print('\nКоличество закрытых issues на заданном периоде времению:\n'.upper())
        print(count_closed_issues(owner, repos))
        print('\nКоличество “старых” issues на заданном периоде времению:\n'.upper())
        print(count_old_issues(owner, repos))

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
