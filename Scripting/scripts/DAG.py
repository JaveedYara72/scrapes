# To initiate the DAG Object
from airflow import DAG
# Importing datetime and timedelta  modules for scheduling the DAGs
from datetime import timedelta, datetime
# Importing operators 
from airflow.operators.dummy_operator import DummyOperator

# Initiating the default args
default_args = {
    'owner' : 'javeed',
    'start_date':datetime(2023,01,25)
}

# creating the DAG object
dag = DAG(
    dag_id = 'DAG_1',
    default_args = default_args,
    schedule_interval = '@once',
    catchup = False
)

# creating the first task
start = DummyOperator(
    task_id = 'first_task',
    dag = dag # this dag is referring to the line 15 dag that i have just initialised.
)

# creating the second task
end = DummyOperator(
    task_id = 'second_rask',
    dag = dag # same dag in line 15
)


# setting up dependencies
start >> end
# this means, start task will run first and end task will run later


