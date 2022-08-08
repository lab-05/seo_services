<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
<title>Проверка выдачи по запросу {{keyword}}</title>
</head>
<body>
%if lenres > 4:
	<h2><span style="color:red">{{keyword}}</span> - Плохой запрос</h2>
	<p>Количество совпадающих доменов {{lenres}}</p><br>
	%for res in result:
	<p>{{res}}</p>
	%end
%else:
	<h2><span style="color:green">{{keyword}}</span> - хороший запрос</h2>
	<p>Количество совпадающих доменов {{lenres}}:
	<ul>
		%for res in result:
		<li>{{res}}</li>
		%end
	</ul>
	</p><hr>
%end


</body>
</html>