<?php 
    $conn = new mysqli('localhost', 'root', '', 'injeksion');
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    function sanitize_input($data) {
        // Trim untuk menghapus spasi di awal/akhir
        // htmlspecialchars untuk mencegah XSS
        return htmlspecialchars(trim($data), ENT_QUOTES, 'UTF-8');
    }

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $username = sanitize_input($_POST['username']);
        $password = sanitize_input($_POST['password']);

        // Gunakan prepared statement untuk menghindari SQL Injection
        $stmt = $conn->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
        $stmt->bind_param("ss", $username, $password); // Bind parameter
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows > 0) {
            echo "Yeayy berhasil! Selamat datang, $username";
        } else {
            echo "Login gagal, username atau password salah.";
        }

        $stmt->close(); // Tutup statement
    }
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Aman</title>
</head>
<body>
    <div class="container">
        <h1>BRI Tablet</h1>
        <form action="" method="POST">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
