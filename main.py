#########################
#   MAIN GAME LOOP      #
#########################
from sokoban import *


def main():
    # Hỏi level từ người chơi
    level_str = start_game()
    matrix, box_weights = map_open(level_str)
    original_game = Game(matrix, box_weights)
    log_debug("Initial game state:")
    original_game.print_matrix()

    # Tạo game hiện hành từ bản sao gốc
    game = copy.deepcopy(original_game)
    size = game.load_size()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    sol = ""
    i = 0
    flagAuto = False
    paused = False  # Biến để kiểm soát pause/resume
    
    # Các biến thống kê để hiển thị (có thể cập nhật từ run_and_measure nếu muốn)
    steps_display = 0
    weight_display = 0
    
    # Vòng lặp chính của GUI
    while True:
        # Vẽ maze lên màn hình
        print_game(game.get_matrix(), screen)
        
        # Hiển thị thống kê (ví dụ ở góc trái trên)
        font = pygame.font.Font(None, 24)
        stats_text = f"Steps: {steps_display}  Weight: {weight_display}"
        stats_surface = font.render(stats_text, True, (0, 0, 0))
        screen.blit(stats_surface, (5, 5))
        
        # Nếu game hoàn thành, hiển thị thông báo và hỏi reset
        if game.is_completed():
            display_end(screen, "Done!")
            # Hiển thị thông báo reset
            display_box(screen, "Reset? (Y/N)")
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            game = copy.deepcopy(original_game)
                            sol = ""
                            i = 0
                            flagAuto = False
                            waiting = False
                        elif event.key == pygame.K_n:
                            waiting = False
                clock.tick(10)
        
        pygame.display.update()
        clock.tick(30)
        
        # Xử lý các sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                # Pause/Resume animation bằng SPACE
                if event.key == pygame.K_SPACE:
                    paused = not paused
                # Chọn thuật toán (phím 1-8)
                elif event.key == pygame.K_1:
                    sol, node_generated = run_and_measure("BFS", BFSsolution, original_game)
                    game = copy.deepcopy(original_game)
                    i = 0
                    flagAuto = True
                elif event.key == pygame.K_2:
                    sol, node_generated = run_and_measure("DFS", DFSsolution, original_game)
                    game = copy.deepcopy(original_game)
                    i = 0
                    flagAuto = True
                elif event.key == pygame.K_3:
                    sol, node_generated = run_and_measure("UCS", UCSsolution, original_game)
                    game = copy.deepcopy(original_game)
                    i = 0
                    flagAuto = True
                elif event.key == pygame.K_4:
                    sol, node_generated = run_and_measure("A*", AstarSolution, original_game)
                    game = copy.deepcopy(original_game)
                    i = 0
                    flagAuto = True
                elif event.key == pygame.K_5:
                    sol, node_generated = run_and_measure("Greedy Best-first Search", GreedyBestFirstSolution, original_game)
                    game = copy.deepcopy(original_game)
                    i = 0
                    flagAuto = True
                elif event.key == pygame.K_6:
                    sol, node_generated = run_and_measure("Dijkstra’s", DijkstraSolution, original_game)
                    game = copy.deepcopy(original_game)
                    i = 0
                    flagAuto = True
                elif event.key == pygame.K_7:
                    sol, node_generated = run_and_measure("Swarm Algorithm", SwarmSolution, original_game)
                    game = copy.deepcopy(original_game)
                    i = 0
                    flagAuto = True
                elif event.key == pygame.K_8:
                    sol, node_generated = run_and_measure("Convergent Swarm Algorithm", ConvergentSwarmSolution, original_game)
                    game = copy.deepcopy(original_game)
                    i = 0
                    flagAuto = True
                # Điều khiển thủ công với mũi tên
                elif event.key == pygame.K_UP:
                    game.move(0, -1, True)
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1, True)
                elif event.key == pygame.K_LEFT:
                    game.move(-1, 0, True)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0, True)
                elif event.key == pygame.K_q:
                    sys.exit(0)
                elif event.key == pygame.K_x:
                    game.unmove()
        
        # Nếu auto-play được bật và không bị pause, tiến hành animation
        if flagAuto and not paused and i < len(sol):
            step = sol[i]
            # Khi auto-play, gọi move_with_cost để cập nhật trạng thái (và tính cost push)
            if step == 'U':
                game.move_with_cost(0, -1, False)
            elif step == 'D':
                game.move_with_cost(0, 1, False)
            elif step == 'L':
                game.move_with_cost(-1, 0, False)
            elif step == 'R':
                game.move_with_cost(1, 0, False)
            i += 1
            # Cập nhật các thống kê hiển thị (có thể lấy từ độ dài sol và replay_solution)
            replay_game = copy.deepcopy(original_game)
            replayed_path, steps, total_weight = replay_solution(replay_game, sol)
            steps_display = steps
            weight_display = total_weight
            if i == len(sol):
                flagAuto = False
            time.sleep(0.2)
            
        if game.is_completed():
            flagAuto = False

if __name__ == "__main__":
    main()
