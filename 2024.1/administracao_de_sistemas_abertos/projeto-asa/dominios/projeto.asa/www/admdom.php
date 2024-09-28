<?php
require 'var_conn.php';

session_start();

if (!($_SESSION["autenticado"]))
        header("Location: index.php");

if ($_SESSION["login"] == 1) {
    
    header("Location: login1.php");
} 

echo "Bem vindo Administrador de Dominio";
echo "<br>Usuario: " . $_SESSION['user']; 
?>
<HTML>
<BODY>
<br>
<TR><TD COLSPAN="4" ALIGN="CENTER">
<button type="button" onclick="window.location.href='sair.php'">SAIR</button>
</TD></TR>
<hr>
<b>Dominios Configurados</b>
<?php

$search = "@";
$pos = strpos($_SESSION['user'], $search);
$dominio = substr($_SESSION['user'], $pos+strlen($search));

$result = $bd->query("SELECT * FROM projeto_users WHERE dominio='$dominio' AND tipo='comum.php'");

echo("
    <TABLE BORDER=1>
    <TR><TH>ID</TH><TH>Usuarios</TH><TH>Remover</TH><TH>Mudar Senha</TH><TH>Senha do usuário</TH></TR>
");

while($line = $result->fetch_assoc()) {
    echo "<TR>";
    echo "<TD>" . $line['uid'] . "</TD>";
    echo "<TD>" . $line['email'] . "</TD>";
    echo "<TD><button type='button' onclick=\"if (confirm('Tem certeza que deseja excluir?')) { window.location.href='rmvusr.php?id=" . $line['uid'] . "'; }\">Remover</button></TD>";
    echo "<TD><button type='button' onclick=\"window.location.href='userpass.php?id=" . $line['uid'] . "';\">Nova senha</button></TD>";
    echo "<TD>" . $line['senha'] . "</TD>";
    echo "</TR>"; 
}

echo "</TABLE>";
 
?>
<form method="post" action="criarusr.php">
<hr>
<b>Criar Usuarios</b>
<br>
    <label for="user id">Novo Usuario:</label>
<br>
    <input type="text" name="novousr" id="user id"> 
<br>
<input type="submit" value="enviar">
</form>
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

