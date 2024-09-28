<?php
session_start();
$_SESSION['autenticado']=0;
$_SESSION['usuario']='vazio';
$_SESSION['userid']=0;
$_SESSION['login']=0;
?>
<html> 
<body> 
  
<form method="post" action="login.php"> 
  <b>LOGIN</b>		
  <br>
  <label for="EMAIL ID">Email:</label>
  <br> 
  <input type="text" name="login" id="Email id"> 
  <br>
  <label for="user-password">Senha: </label>
  <br> 
  <input type="password" name="senha"   id="user-password"> 
  <hr>
  <input type="submit" value="enviar"> 
</form>  
</body> 
</html> 


 
