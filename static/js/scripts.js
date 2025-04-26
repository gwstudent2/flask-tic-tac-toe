document.addEventListener('DOMContentLoaded', () => {
    const cells = document.querySelectorAll('.cell');
    const currentPlayerDisplay = document.getElementById('current-player');
    const gameOverMessage = document.getElementById('game-over-message');
    const resetButton = document.getElementById('reset-button');

    cells.forEach(cell => {
        cell.addEventListener('click', () => {
            const row = cell.getAttribute('data-row');
            const col = cell.getAttribute('data-col');

            fetch('/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ row, col })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    cell.textContent = currentPlayerDisplay.textContent.includes('X') ? 'X' : 'O';
                    currentPlayerDisplay.textContent = `Current Player: ${data.current_player}`;

                    if (data.winner) {
                        gameOverMessage.textContent = `Player ${data.winner} wins!`;
                        highlightWinningCombination(data.winning_combination);
                    } else if (data.draw) {
                        gameOverMessage.textContent = 'It\'s a draw!';
                    }
                }
            });
        });
    });

    resetButton.addEventListener('click', () => {
        fetch('/reset', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'Game reset') {
                cells.forEach(cell => {
                    cell.textContent = '';
                    cell.classList.remove('winning-cell');
                });
                currentPlayerDisplay.textContent = 'Current Player: X';
                gameOverMessage.textContent = '';
            }
        });
    });

    function highlightWinningCombination(combination) {
        combination.forEach(([row, col]) => {
            const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
            cell.classList.add('winning-cell');
        });
    }
});
