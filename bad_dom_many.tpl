<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

    <!--<title>Проверка выдачи по запросам {#{keyword}}</title>-->
</head>
<body>
<div class="container">

    <div class="py-5 text-center">
      <h2>Результат проверки запросов</h2>
      <p class="lead">В таблицах ниже результат проверки</p>
    </div>
      <div class="card-deck mb-3 text-center">
    <table class="table table-bordered">
        <thead class="thead-dark">
        <tr>
            <th scope="col">Запрос</th>
            <th scope="col">Количество совпадающих доменов</th>
            <th scope="col">Совпадающие домены</th>
        </tr>
        </thead>
%for keyw, keywres in keywdict.items():
        <tbody>
        <tr>
        %if len(keywres) >= 4:
            <td style="color:red">{{keyw}}</td>
            <td>{{len(keywres)}}</td>
            <td>
            %for concurent in keywres:
                {{concurent}}<br>
            %end
            </td>
        %end
        </tr>
        </tbody>
%end
    </table>
<br><br>
    <table class="table table-bordered">
        <thead class="thead-dark">
        <tr>
            <th scope="col">Запрос</th>
            <th scope="col">Количество совпадающих доменов</th>
            <th scope="col">Совпадающие домены</th>
        </tr>
        </thead>
%for keyw, keywres in keywdict.items():
        <tbody>
        <tr>
        %if len(keywres) < 4:
            <td style="color:green">{{keyw}}</td>
            <td>{{len(keywres)}}</td>
            <td>
            %for concurent in keywres:
                {{concurent}}<br>
            %end
            </td>
        %end
        </tr>
        </tbody>
%end
    </table>
      </div>
</div>
</body>

</html>