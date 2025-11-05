import streamlit as st
import json
import datetime
from pathlib import Path
import streamlit.components.v1 as components

# initialize session state for version selection
if 'version_selected' not in st.session_state:
    st.session_state.version_selected = None

def select_fun_version():
    st.session_state.version_selected = 'fun'

def select_professional_version():
    st.session_state.version_selected = 'professional'

# show buttons only if no version selected yet
if st.session_state.version_selected is None:
    st.title("Welcome! Choose Your Experience")
    col1, col2 = st.columns(2)
    with col1:
        st.button('🎮 Fun version', on_click=select_fun_version, use_container_width=True)
    with col2:
        st.button('💼 Professional version', on_click=select_professional_version, use_container_width=True)
    st.stop()

# -------------- FUN VERSION CONTENT -----------------------
if st.session_state.version_selected == 'fun':
    # Initialize session state for flappy bird interface
    if 'unlocked' not in st.session_state:
        st.session_state.unlocked = False

    # ------------- Flappy Bird Unlock Interface
    if not st.session_state.unlocked:
        st.title("🔒 Unlock My CV")
        st.write("Score 3 points in Flappy Bird to unlock! Click the screen or press SPACE to jump.")
            
        # Create a checkbox that will be toggled by JavaScript
        unlock_checkbox = st.checkbox("Unlocked", value=False, key="unlock_check", label_visibility="hidden")
        
        if unlock_checkbox:
            st.session_state.unlocked = True
            st.rerun()
        
        # Flappy Bird game HTML
        flappy_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    margin: 0;
                    padding: 20px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    height: 700px;
                    font-family: Arial, sans-serif;
                }
                #board {
                    background-color: #70c5ce;
                    box-shadow: 0 0 20px rgba(0,0,0,0.3);
                    cursor: pointer;
                }
                #victory-message {
                    display: none;
                    text-align: center;
                    color: white;
                    font-size: 32px;
                }
                #victory-message h1 {
                    font-size: 48px;
                    margin-bottom: 20px;
                }
            </style>
        </head>
        <body>
            <canvas id="board"></canvas>
            <div id="victory-message"></div>
            
            <script>
                //board
                let board;
                let boardWidth = 360;
                let boardHeight = 640;
                let context;

                //bird
                let birdWidth = 34;
                let birdHeight = 24;
                let birdX = boardWidth/8;
                let birdY = boardHeight/2;

                let bird = {
                    x : birdX,
                    y : birdY,
                    width : birdWidth,
                    height : birdHeight
                }

                //pipes
                let pipeArray = [];
                let pipeWidth = 64;
                let pipeHeight = 512;
                let pipeX = boardWidth;
                let pipeY = 0;

                //physics
                let velocityX = -2;
                let velocityY = 0;
                let gravity = 0.4;

                let gameOver = false;
                let score = 0;
                let messageSent = false;

                window.onload = function() {
                    board = document.getElementById("board");
                    board.height = boardHeight;
                    board.width = boardWidth;
                    context = board.getContext("2d");

                    // Draw simple bird (yellow circle)
                    drawBird();

                    requestAnimationFrame(update);
                    setInterval(placePipes, 1500);
                    document.addEventListener("keydown", moveBird);
                    
                    // Add click event listener to the canvas
                    board.addEventListener("click", function() {
                        jump();
                    });
                    
                    // Add touch event listener for mobile
                    board.addEventListener("touchstart", function(e) {
                        e.preventDefault();
                        jump();
                    });
                }

                function drawBird() {
                    context.fillStyle = "#FFD700";
                    context.beginPath();
                    context.arc(bird.x + bird.width/2, bird.y + bird.height/2, bird.width/2, 0, Math.PI * 2);
                    context.fill();
                    
                    // Eye
                    context.fillStyle = "black";
                    context.beginPath();
                    context.arc(bird.x + bird.width/2 + 5, bird.y + bird.height/2 - 3, 3, 0, Math.PI * 2);
                    context.fill();
                }

                function update() {
                    requestAnimationFrame(update);
                    if (gameOver) {
                        return;
                    }
                    context.clearRect(0, 0, board.width, board.height);

                    //bird
                    velocityY += gravity;
                    bird.y = Math.max(bird.y + velocityY, 0);
                    drawBird();

                    if (bird.y > board.height) {
                        gameOver = true;
                    }

                    //pipes
                    for (let i = 0; i < pipeArray.length; i++) {
                        let pipe = pipeArray[i];
                        pipe.x += velocityX;
                        
                        // Draw pipe
                        context.fillStyle = pipe.isTop ? "#2ecc71" : "#27ae60";
                        context.fillRect(pipe.x, pipe.y, pipe.width, pipe.height);
                        
                        // Draw pipe border
                        context.strokeStyle = "#1e8449";
                        context.lineWidth = 3;
                        context.strokeRect(pipe.x, pipe.y, pipe.width, pipe.height);

                        if (!pipe.passed && bird.x > pipe.x + pipe.width) {
                            score += 0.5;
                            pipe.passed = true;
                            
                            if (score >= 3 && !messageSent) {
                                messageSent = true;
                                
                                // Hide the game canvas
                                board.style.display = 'none';
                            }
                        }

                        if (detectCollision(bird, pipe)) {
                            // only unlock CV when player has score >= 3 AND collides
                            if (messageSent == true) {
                                gameOver = true; // stop movement for a moment
                                messageSent = true;

                                // Show victory message
                                let victoryDiv = document.getElementById('victory-message');
                                victoryDiv.innerHTML = '<h1>🎉 YOU WIN! 🎉</h1><p>Unlocking CV...</p>';
                                victoryDiv.style.display = 'block';

                                // Unlock the CV
                                setTimeout(() => {
                                    try {
                                        const checkbox = window.parent.document.querySelector('input[type="checkbox"]');
                                        if (checkbox && !checkbox.checked) {
                                            checkbox.click();
                                        }
                                    } catch(e) {
                                        console.log('Could not access parent checkbox:', e);
                                    }
                                }, 1500);
                            } else {
                                // Regular game over if score < 3
                                gameOver = true;
                            }
                        }

                    }

                    //clear pipes
                    while (pipeArray.length > 0 && pipeArray[0].x < -pipeWidth) {
                        pipeArray.shift();
                    }

                    //score
                    context.fillStyle = "white";
                    context.font="45px sans-serif";
                    context.fillText(score, 5, 45);

                    if (gameOver && score < 3) {
                        context.fillStyle = "white";
                        context.font="35px sans-serif";
                        context.fillText("GAME OVER", 50, boardHeight/2);
                        context.font="20px sans-serif";
                        context.fillText("Click to restart", 80, boardHeight/2 + 40);
                    }
                }

                function placePipes() {
                    if (gameOver) {
                        return;
                    }

                    let randomPipeY = pipeY - pipeHeight/4 - Math.random()*(pipeHeight/2);
                    let openingSpace = board.height/4;

                    let topPipe = {
                        x : pipeX,
                        y : randomPipeY,
                        width : pipeWidth,
                        height : pipeHeight,
                        passed : false,
                        isTop: true
                    }
                    pipeArray.push(topPipe);

                    let bottomPipe = {
                        x : pipeX,
                        y : randomPipeY + pipeHeight + openingSpace,
                        width : pipeWidth,
                        height : pipeHeight,
                        passed : false,
                        isTop: false
                    }
                    pipeArray.push(bottomPipe);
                }

                function jump() {
                    //jump
                    velocityY = -6;

                    //reset game
                    if (gameOver && score < 3) {
                        bird.y = birdY;
                        pipeArray = [];
                        score = 0;
                        gameOver = false;
                        messageSent = false;
                    }
                }

                function moveBird(e) {
                    if (e.code == "Space" || e.code == "ArrowUp" || e.code == "KeyX") {
                        jump();
                    }
                }

                function detectCollision(a, b) {
                    return a.x < b.x + b.width &&
                        a.x + a.width > b.x &&
                        a.y < b.y + b.height &&
                        a.y + a.height > b.y;
                }
            </script>
        </body>
        </html>
        """
        
        components.html(flappy_html, height=750)
        
        # Button fallback
        st.write("---")
        if st.button("Skip Game ⏩"):
            st.session_state.unlocked = True
            st.rerun()

        if st.button("Change versions 🔁"):
            st.session_state.version_selected = None
            st.rerun()
        
        st.stop()

    # ------------- CV content (shown after unlock)
    st.title("✨ My Interactive CV")

    # Load data.json file
    try:
        with open("data.json", "r") as f:
            entries = json.load(f)
    except FileNotFoundError:
        st.error("data.json file not found!")
        st.stop()

    # Parse available dates
    all_dates = []
    for k in entries:
        try:
            all_dates.append(datetime.datetime.strptime(k, "%d-%m-%Y").date())
        except ValueError:
            try:
                all_dates.append(datetime.datetime.strptime(k, "%m-%Y").date())
            except ValueError:
                try:
                    all_dates.append(datetime.datetime.strptime(k, "%Y").date())
                except ValueError:
                    pass

    all_dates = sorted(all_dates)
    if not all_dates:
        st.warning("No valid entries found in data.json.")
        st.stop()

    # Slider
    date = st.select_slider(
        "📅 Pick a date",
        options=all_dates,
        value=all_dates[-1],
        format_func=lambda d: d.strftime("%B %Y"),
    )

    formats_to_try = ["%d-%m-%Y", "%m-%Y", "%Y"]
    date_str = None
    for fmt in formats_to_try:
        ds = date.strftime(fmt)
        if ds in entries:
            date_str = ds
            break

    # Display corresponding content
    if date_str and date_str in entries:
        file_path = Path(entries[date_str])
        if file_path.exists():
            st.markdown(file_path.read_text(), unsafe_allow_html=True)
        else:
            st.subheader(f"📅 {date.strftime('%d %B %Y')}")
            st.write(entries[date_str])
    else:
        st.info("Nothing recorded for this date.")

    # Reset button at the bottom
    st.write("---")
    if st.button("🔒 Lock CV"):
        st.session_state.unlocked = False
        st.rerun()

# -------------- PROFESSIONAL VERSION CONTENT -----------------------
elif st.session_state.version_selected == 'professional':
    st.title("💼 Professional CV")
    st.write("Welcome to the professional version!")

    #Display professional version here
    st.write("Nothing professional here yet 👀")
    if st.button("Change versions 🔁"):
        st.session_state.version_selected = None
        st.rerun()
    st.stop()