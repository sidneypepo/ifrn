<?php
session_start();

if (!($_SESSION["autenticado"]))
        header("Location: index.php");

if ($_SESSION["login"] == 1) {
    
    header("Location: login1.php");
} 

echo "Bem vindo";
echo "<br>Usuario: " . $_SESSION['user']
?>
<HTML>
<BODY>
<br>
<TR><TD COLSPAN="4" ALIGN="CENTER">
<button type="button" onclick="window.location.href='sair.php'">SAIR</button>
</TD></TR>
<form method="post" action="trocasenha.php">
<hr>
<b>Trocar Senha</b>
<br>
    <label for="pass id">Nova Senha:</label>
<br>
    <input type="text" name="novasenha" id="pass id">
<br>
<input type="submit" value="enviar">
</form>
</BODY>
</HTML>


