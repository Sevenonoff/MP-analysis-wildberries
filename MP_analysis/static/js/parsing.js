document.getElementById('parse-form').addEventListener('submit', function (event) {
    event.preventDefault(); 

    const searchQuery = document.getElementById('search_query').value;

    fetch('http://localhost:8000/api/parse/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ search_query: searchQuery }),
    })
    .then(response => response.json())
    .then(data => {
        alert('Парсинг завершен!');
        window.location.reload();
    })
    .catch(error => {
        console.error('Ошибка при парсинге:', error);
        alert('Произошла ошибка при парсинге.');
    });
});