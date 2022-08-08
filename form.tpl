<html>
<head>
<meta charset="utf-8">
    <!--https://www.bootstrapcdn.com/-->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

<title>Проверка выдачи по запросу</title>
</head>
<body>

<div class="container">
  <main>
    <div class="py-5 text-center">
      <h2>Проверка запросов</h2>
      <p class="lead">Введите список запросов для проверки их на предмет качества и количества агрегаторов в выдаче</p>
    </div>

    <div class="row g-5">
      <div class="col-md-7 col-lg-8">
        <h4 class="mb-3">Список слов</h4>
          <div class="input-group has-validation">
            <form action="/bad_domains" method="post" class="needs-validation" novalidate="">
                <textarea name="keyword" class="form-control"></textarea><br>
                <input value="search" type="submit" class="w-100 btn btn-primary btn-lg" />
            </form>
              </div>
      </div>
    </div>
  </main>
</div>
</body>
</html>
