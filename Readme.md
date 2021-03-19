Python MS LAPS implementation
Для сборки и запуска проекта потребуеться установка следующих модулей:
1) ldap3
2) Ping3
3) TKinter
Так же, нужна версия Python 3.7 - 3.9.1

Установка модулей:
1) pip install ldap3
2) pip install Ping3
3) pip install tkinter

Полный список подключенных модулей:
1) tkinter (Нужен для построения графического интерфейса)
2) os (Модуль отвечающий за связь с ОС)
3) datetime
4) socket (Модуль для работы с сетью)
5) re (Модуль подключает поддержку регулярных выражений PCRE(Perl Compatible Regular Expression))

Инструкция:
Кнопка <<Load>> Загружает ранее созданый профиль из файла.

Кнопка <<Save>> Сохраняет данные(Имя/пароль) в шифрованом виде в файл профиля.

Кнопка <<Get Password>> Возвращает пароль rml от УЗ компьютера и пишет его в поле.