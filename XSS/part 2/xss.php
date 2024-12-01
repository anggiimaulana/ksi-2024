<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulasi XSS</title>
</head>
<body>
    <h1>Masukan Komentar:</h1>
    <form action="" method="post">
        <label for="nama">Nama:</label>
        <input type="text" id="nama" name="name">
        <label for="komentar">Komentar:</label>
        <textarea name="comment" id="komentar"></textarea>
        <button type="submit">Kirim</button>
    </form>

    <h2>Komentar Sebelumnya:</h2>

    <?php
        session_start();
        if (!isset($_SESSION['comment'])) {
            $_SESSION['comment'] = [];
        }

        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $name = htmlspecialchars($_POST['name'], ENT_QUOTES, 'UTF-8');  // Sanitize name input
            $comment = htmlspecialchars($_POST['comment'], ENT_QUOTES, 'UTF-8');  // Sanitize comment input

            $_SESSION['comment'][] = [
                'name' => $name,
                'comment' => $comment
            ];
        }

        foreach ($_SESSION['comment'] as $comment) {
            echo "<p><strong>" . $comment['name'] . ":</strong> " . $comment['comment'] . "</p>";
        }
    ?>
</body>
</html>
