## Типы связей между таблицами в схеме

![](../img/cinema_schema_diagram.png)

|  Тип связи  | Таблица 1 | Таблица 2       |
|:-----------:|-----------|-----------------|
|     1:N     | actors    | movie_cast      |
|     1:N     | movie     | movie_cast      |
|     1:N     | movie     | movie_direction |
|     1:N     | movie     | oscar_awarded   |
|     1:N     | director  | movie_direction |
