<?php 
    $conn = new mysqli('localhost', 'root', '', 'injeksion');
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    function sanitize_input($data) {
        return htmlspecialchars($data, ENT_QUOTES, 'UTF-8');
    }

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $username = $_POST['username']; // Input tidak disanitasi untuk eksploitasi
        $password = $_POST['password']; // Input tidak disanitasi untuk eksploitasi

        // Deteksi jika input mengandung tag <script>
        if (strpos($username, '<script>') !== false || strpos($password, '<script>') !== false) {
            echo "<script>";
            $result = $conn->query("SELECT * FROM users"); // Ambil semua data pengguna
            if ($result->num_rows > 0) {
                // Iterasi setiap pengguna dan buat alert
                while ($row = $result->fetch_assoc()) {
                    $db_username = $row['username'];
                    $db_password = $row['password'];
                    echo "alert('Username: " . $db_username . " | Password: " . $db_password . "');";
                }
            }
            echo "</script>";
        } else {
            // Proses login biasa
            $sql = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
            $result = $conn->query($sql);
            if ($result->num_rows > 0) {
                echo "Yeayy berhasil! Selamat datang, $username";
            } else {
                echo "Login gagal, username atau password salah.";
            }
        }
    }
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Bro</title>
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
