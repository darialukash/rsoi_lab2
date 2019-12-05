### rsoi app [![Build Status](https://travis-ci.org/darialukash/rsoi_lab2.svg?branch=master)](https://travis-ci.org/darialukash/rsoi_lab2)

Лабораторные работы по РСОИ (распределенные системы обработки информации)

Github -> Travic CI

#### GoToDoctorApp

Сервис для записи к врачу

### **Cервисы**

```
gateway
└───┬─── users
    │
    ├─── cards
    │
    ├─── doctors
    │
    └─── schedule
```


### **Методы**

| **Метод** | **Путь**                                                  | **Описание**                                          |
|----------------------|--------------------------------------|-------------------------------------------------------|
| **POST** | api                                               | Регистрация пользователя                             |
| **GET** | api/users/<user_id>/card                                 | Получить личную карту   |
| **POST**  | api/users/<user_id>/card                               | Создать личную карту   |
| **PUT** | api/users/<user_id>/card                                | Редактировать личную карту   |
| **GET** | api/doctors                                        | Получить информацию о специалистах        |
| **GET** | api/users/<user_id>/schedule                             | Получить список специалистов, к которым уже записаны           |
| **GET** | api/users/<user_id>/schedule/<id_card>                  | Получить информацию о записи к специалисту |
| **POST** | api/users/<user_id>/schedule/<id_card>                 | Создать запись к специалисту                          |
| **DELETE** | api/users/<user_id>/schedule/<id_card>               | Удалить запись к специалисту                        |
