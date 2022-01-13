# airflow-experiments
There are 6 different ways of creating variables in Airflow 😱

+ Airflow UI   👌
+ Airflow CLI 👌
+ REST API 👌
+ Environment Variables ❤️
+ Secret Backend ❤️
+ Programatically 😖
Whether to choose one way or another depends on your use case and what you prefer.

Overall, by creating a variable  with an environment variable you

+ avoid making a connection to your DB
+ hide sensitive values (you variable can be fetched only within a DAG)

Notice that it is possible to create connections with environment variables. You just have to export the env variable:

```AIRFLOW_CONN_NAME_OF_CONNECTION=your_connection```

and get the same benefits as stated previously.

Ultimately, if you really want a secure way of storing your variables or connections, use a Secret Backend.

To learn more about this, click on this [link](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/secrets-backend/index.html)

Finally, here is the order in which Airflow checks if your variable/connection exists:
[](images/envs.png)
