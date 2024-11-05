function openModal(name, gender, species, breed, age, healthStatus, animalId) {
    document.getElementById('modalAnimalName').textContent = name;
    document.getElementById('modalAnimalDetails').textContent = `
        Гендер: ${gender},
        Вид: ${species},
        Порода: ${breed},
        Вік: ${age} р.,
        Стан здоров'я: ${healthStatus}
    `;

    // Зберігаємо id тварини у кнопці
    const adoptButton = document.getElementById('adoptButton');
    adoptButton.setAttribute('onclick', `window.location.href='/adopt_animal/${animalId}/'`);

    // Відкриваємо модальне вікно
    document.getElementById('animalModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('animalModal').style.display = 'none';
}
