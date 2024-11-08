// Функція для відкриття модального вікна
function openModal(name, gender, species, breed, age, healthStatus, animalId) {
    document.getElementById('modalAnimalName').textContent = name;
    document.getElementById('modalAnimalDetails').textContent = `
        Гендер: ${gender},
        Вид: ${species},
        Порода: ${breed},
        Вік: ${age} р.,
        Стан здоров'я: ${healthStatus}
    `;

    // Перевірка ID тварини
    if (animalId !== undefined && animalId !== null) {
        const adoptButton = document.getElementById('adoptButton');
        adoptButton.setAttribute('onclick', `window.location.href='/shelter/adopt_animal/${animalId}'`);
    } else {
        console.error("animalId is undefined");
    }

    // Відкриваємо модальне вікно
    document.getElementById('animalModal').style.display = 'block';
}

// Функція для закриття модального вікна
function closeModal() {
    document.getElementById('animalModal').style.display = 'none';
}
