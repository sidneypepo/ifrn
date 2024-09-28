<?php
require 'var_conn.php';

session_start();

if (!($_SESSION["autenticado"]))
        header("Location: index.php");

echo "Bem vindo Administrador Geral";
echo "<br>Usuario: " . $_SESSION['user'] 
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

$result = $bd->query("SELECT *,senha FROM domains, projeto_users WHERE email LIKE 'root@%'");

echo("
    <TABLE BORDER=1>
    <TR><TH>Dominio</TH><TH>Editar</TH><TH>Senha do root</TH></TR>
");

while($line = $result->fetch_assoc()) {
    echo "<TR>";
    echo "<TD>" . $line['domain'] . "</TD>";
    echo "<TD><button type='button' onclick=\"if (confirm('Tem certeza que deseja excluir?')) { window.location.href='rmvdom.php?dom=" . $line['domain'] . "'; }\">Remover</button></TD>";
    echo "<TD>" . $line['senha'] . "</TD>";
    echo "</TR>"; 
}

echo "</TABLE>";
 
?>
<form method="post" action="criardom.php">
<hr>
<b>Criar Dominios</b>
<br>
    <label for="dom id">Novo dominio:</label>
<br>
    <input type="text" name="novodom" id="dom id"> 
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

