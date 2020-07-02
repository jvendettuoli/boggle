class Boggle {
	constructor(gameTimeSecs = 60) {
		this.gameTimeSecs = gameTimeSecs;
		this.score = 0;
		this.attemptedWords = new Set();
		this.scoredWords = new Set();

		//Show time and set timer interval
		this.displayTimer();
		this.timer = setInterval(this.timerCount.bind(this), 1000);

		//Event handler for submit event
		$('#word-form').on('submit', this.submitWord.bind(this));
	}

	//Called on submit event. Sends word to server for validation.
	async submitWord(evt) {
		evt.preventDefault();

		//get word and reset form
		const $wordInput = $('#word-input');
		const word = $wordInput.val().toLowerCase();
		$('#word-form').trigger('reset');

		//send submitted word to server for validation
		const res = await axios.get('/check-word', { params: { word } });
		const result = res.data.result;

		//score word depending on result
		this.scoreWord(word, result);

		//display result to user
	}

	//Handles scoring a given word based on validation result returned by server
	async scoreWord(word, result) {
		console.log(word, result);
		//only score words that are valid and on board, otherwise display why word is not scored
		const results = {
			'not-on-board' : () => {
				$('#result').text(result);
				this.attemptedWords.add(word);
			},
			ok             : () => {
				//catch if word has been used
				if (this.scoredWords.has(word)) {
					$('#result').text('Word already scored.');
					return;
				}
				//update score
				$('#result').text(result);
				this.updateScore(word);
				this.displayScore();
				this.scoredWords.add(word);
			},
			'not-word'     : () => {
				$('#result').text(result);
				this.attemptedWords.add(word);
			}
		};

		results[result]();
	}

	//update score based on valid word length
	async updateScore(word) {
		const wordScore = word.length;
		this.score += wordScore;
	}

	//display score to user
	displayScore() {
		$('#score-container').text(this.score);
	}

	timerCount() {
		this.gameTimeSecs -= 1;
		this.displayTimer();
		if (this.gameTimeSecs === 0) {
			//hide word form to prevent additional entries
			$('#word-form').hide();
			clearInterval(this.timer);

			//send score to server
			this.updateUserStats();
		}
	}
	displayTimer() {
		$('#timer-container').text(this.gameTimeSecs);
	}

	async updateUserStats() {
		//send submitted end score to server for saving
		const res = await axios.post('/save-stats', { score: this.score });
		const result = res.data;
		console.log(result);
	}
}
