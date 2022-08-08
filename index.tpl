<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
<title>Список SEO сервисов</title>
</head>
<body>
<h2 style="color:#f00;">{{names}}</h2>
<br>
<h3>{{url_result}}</h3>
% for i in range(3):
	<h4>{{keyword}}</h4>
% end
</ul>
</body>
</html>