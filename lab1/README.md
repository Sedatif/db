# Лабораторна робота №1

**Проектування бази даних та ознайомлення з базовими операціями СУБД PostgreSQL**

##### виконав Суходольський Євгеній Віталійович група КП-82 Варіант 18

1. Модель «сутність-зв’язок» предметної галузі

   ![V](https://res.cloudinary.com/nicereadcloud/image/upload/v1601145438/library_jqpyt8.png)
   
2. Структура нормалізованої бази даних з назвами таблиць та зв’язками між ними

   ![V](https://res.cloudinary.com/nicereadcloud/image/upload/v1601148615/relations_honb48.jpg)
       
| Сутність | Атрибут | Тип даних |
|----------|-----------|-----------|
| author | `author_id` - унікальний ідентифікатор автора<br>`fullname` - повне ім'я автора<br>`birth_date` - дата народження автора<br>`country` - країна, в якій народився автор | Integer<br>String<br>Date<br>String|
Book | `book_id` - унікальний ідентифікатор книги<br>`name` - назва книги<br>`publish_date` - дата випуску книги<br>`quantity` - кількість копій, що є в наявності в бібліотеці<br>`author_id` - унікальний ідентифікатор автора| Integer<br>String<br>Date<br>String<br>Integer|
Reader |`reader_id` - унікальний ідентифікатор читача<br>`fullname` - повне ім'я читача<br>`address` - адреса проживання читача| Integer<br>String<br>String|
Subscription | `subscription_id` - унікальний ідентифікатор абонементу<br>`start_date` - дата початку дії абонементу<br>`end_date` - дата завершення дії абонементу<br>`reader_id` - унікальний ідентифікатор читача | Integer<br>Date<br>Date<br>Integer |
Books_subscriptions | `books_subscriptions_id` - унікальний ідентифікатор зв'язку книги з абонементом<br>`subscription_id` - унікальний ідентифікатор абонементу<br>`book_id` - унікальний ідентифікатор книги | Integer<br>Integer<br>Integer |
   
3. Копії екранних форм (screenshots) вмісту таблиць бази даних з pgAdmin4
   
      Authors
      
      ![V](https://res.cloudinary.com/nicereadcloud/image/upload/v1601145884/authors_dybj73.jpg)
   
      Books
      
      ![V](https://res.cloudinary.com/nicereadcloud/image/upload/v1601145883/books_dvlkaf.jpg)
   
      Readers
      
      ![V](https://res.cloudinary.com/nicereadcloud/image/upload/v1601145883/readers_g6k8at.jpg)
   
      Subscriptions
      
      ![V](https://res.cloudinary.com/nicereadcloud/image/upload/v1601145883/subs_nvh51v.jpg)
      
      Book_subscription_links
      
      ![V](https://res.cloudinary.com/nicereadcloud/image/upload/v1601145883/links_gjrdsc.jpg)
