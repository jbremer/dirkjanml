<?php

$secret = '';

$to       = '';
$from     = '';

$msg = '
<html>
  <head>
    <title>Dirkjan - '.$_GET['title'].'</title>
  </head>
  <body>
    <p>
Dear Dirkjan Reader, <br /><br />

Following is the latest Dirkjan! As usual, enjoy the rest of your day.
<br />

<h3>'.$_GET['title'].'</h3><br />

<img src="'.$_GET['url'].'" /> <br /><br />

If your email client does not show an inline image, please open the <br />
following link which will lead you to the image directly. <br /><br />
<a href="'.$_GET['url'].'">'.$_GET['url'].'</a> <br /><br />

Regards, <br />
Jurriaan <br /> <br />

ps: I\'m not affiliated with Veronica in any way. Any damage done <br />
through this email is at your own responsibility. I do not intend <br />
to damage Veronica in any way.
    </p>
  </body>
</html>
';

$headers  = 'MIME-Version: 1.0'."\r\n";
$headers .= 'Content-type: text/html; charset=iso-8859-1'."\r\n";
$headers .= 'From: '.$from."\r\n";

if($_GET['secret'] === $secret) {
    mail($to, $_GET['title'], $msg, $headers);
}

?>
