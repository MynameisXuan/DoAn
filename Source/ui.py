import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import time
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        # PyInstaller tạo folder tạm và giải nén file vào đây
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    full_path = os.path.join(base_path, relative_path)
    print(f"[DEBUG] Looking for file: {full_path}")  # Debug
    print(f"[DEBUG] File exists: {os.path.exists(full_path)}")  # Debug
    return full_path

class MazeSelectionScreen:
    """Screen for selecting which maze to solve"""
    
    def __init__(self, root, on_select_callback):
        self.root = root
        self.on_select = on_select_callback
        self.frame = tk.Frame(root, bg="#87CEEB")
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.create_ui()
    
    def create_ui(self):
        """Create the maze selection interface"""
        main_container = tk.Frame(self.frame, bg="#87CEEB")
        main_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        title_frame = tk.Frame(main_container, bg="#2c3e50", bd=8, relief=tk.RIDGE)
        title_frame.pack(pady=30)
        
        title = tk.Label(
            title_frame,
            text="THE BABY DUCKLING'S ADVENTURE!",
            font=("Comic Sans MS", 28, "bold"),
            bg="#2c3e50",
            fg="#FFD700",
            padx=40,
            pady=20
        )
        title.pack()
        
        subtitle = tk.Label(
            main_container,
            text="Choose a reed field to help the baby duckling",
            font=("Arial", 16, "italic"),
            bg="#87CEEB",
            fg="#2c3e50"
        )
        subtitle.pack(pady=10)
        
        self.maze_files = [
            ("input1.txt", "Level 1", "#90EE90", "12×15"),
            ("input2.txt", "Level 2", "#FFD700", "15×15"),
            ("input3.txt", "Level 3", "#FFA500", "15×15"),
            ("input4.txt", "Level 4", "#FF69B4", "18×18"),
            ("input5.txt", "Level 5", "#9370DB", "22×22"),
            ("input6.txt", "Level 6", "#FF6347", "25×25")
        ]
        
        button_container = tk.Frame(main_container, bg="#2c3e50", bd=8, relief=tk.RIDGE)
        button_container.pack(pady=20)
        
        button_inner = tk.Frame(button_container, bg="#34495e")
        button_inner.pack(padx=15, pady=15)
        
        for i, (filename, label, color, size) in enumerate(self.maze_files):
            row = i // 3
            col = i % 3
            
            btn_frame = tk.Frame(button_inner, bg=color, bd=4, relief=tk.RAISED)
            btn_frame.grid(row=row, column=col, padx=12, pady=12)
            
            btn = tk.Button(
                btn_frame,
                text=label,
                font=("Comic Sans MS", 12, "bold"),
                bg=color,
                fg="#2c3e50",
                width=20,
                height=2,
                command=lambda f=filename: self.select_maze(f),
                cursor="hand2",
                bd=0,
                wraplength=180
            )
            btn.pack(pady=5)
            
            size_label = tk.Label(
                btn_frame,
                text=f"Size: {size}",
                font=("Arial", 9),
                bg=color,
                fg="#2c3e50"
            )
            size_label.pack()
        
        control_frame = tk.Frame(main_container, bg="#87CEEB")
        control_frame.pack(pady=20)
        
        exit_btn = tk.Button(
            control_frame,
            text="✖ Exit Game",
            font=("Arial", 13, "bold"),
            bg="#e74c3c",
            fg="black",
            padx=30,
            pady=12,
            command=self.exit_app,
            cursor="hand2",
            bd=3,
            relief=tk.RAISED
        )
        exit_btn.pack()
    
    def select_maze(self, filename):
        """Handle maze selection"""
        file_path = resource_path(filename)
        print(f"[DEBUG] Selecting maze: {filename}")
        print(f"[DEBUG] Full path: {file_path}")
        print(f"[DEBUG] Exists: {os.path.exists(file_path)}")
        
        if not os.path.exists(file_path):
            # List all files in the directory for debugging
            try:
                base_path = sys._MEIPASS
            except:
                base_path = os.path.abspath(".")
            
            files_in_dir = os.listdir(base_path)
            print(f"[DEBUG] Files in directory: {files_in_dir}")
            
            messagebox.showerror(
                "🚫 Oops! File Not Found", 
                f"Oh no! The file '{filename}' flew away! 🦆\n\n"
                f"Looking in: {base_path}\n"
                f"Full path: {file_path}\n\n"
                f"Files found: {', '.join(files_in_dir)}"
            )
            return
        
        self.on_select(filename)
    
    def exit_app(self):
        """Exit the application"""
        if messagebox.askokcancel("Exit", "Are you sure you want to abandon the duckling? 🥺"):
            self.root.quit()
    
    def destroy(self):
        """Clean up the frame"""
        self.frame.destroy()

class MazeUI:
    def __init__(self, root, filename):
        self.root = root
        self.selected_file = filename
        self.maze_data = []
        self.path_data = []
        self.rows = 0
        self.cols = 0
        self.cell_size = 40
        self.zoom_level = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 2.0
        self.offset_x = 0
        self.offset_y = 0
        self.has_entrance = False
        self.has_exit = False
        self.animation_running = False
        self.current_step = 0
        self.duck_sprite = None
        
        self.frame = tk.Frame(root, bg="#E8F4F8")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.load_maze(filename)
        self.create_widgets()
        self.draw_maze()
    
    def create_widgets(self):
        title_frame = tk.Frame(self.frame, bg="#2E86AB")
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="THE BABY DUCKLING IS LOST IN THE REED FIELD",
            font=("Comic Sans MS", 22, "bold"),
            bg="#2E86AB",
            fg="white",
            pady=12
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="💚 Help the baby duckling find its mother! 💚",
            font=("Arial", 13, "italic"),
            bg="#2E86AB",
            fg="#E8F4F8",
            pady=5
        )
        subtitle_label.pack()
        
        button_frame = tk.Frame(self.frame, bg="#E8F4F8")
        button_frame.pack(pady=15)
        
        self.solve_btn = tk.Button(
            button_frame,
            text="🦆 Help the Duckling!",
            font=("Comic Sans MS", 11, "bold"),
            bg="#27ae60",
            fg="black",
            activebackground="#229954",
            padx=20,
            pady=10,
            command=self.solve_maze,
            cursor="hand2",
            state=tk.NORMAL
        )
        self.solve_btn.grid(row=0, column=0, padx=8)
        
        self.back_btn = tk.Button(
            button_frame,
            text="🏠 Back to Pond",
            font=("Comic Sans MS", 11, "bold"),
            bg="#3498db",
            fg="black",
            activebackground="#2980b9",
            padx=20,
            pady=10,
            command=self.back_to_selection,
            cursor="hand2"
        )
        self.back_btn.grid(row=0, column=1, padx=8)
        
        self.restart_btn = tk.Button(
            button_frame,
            text="🔄 Clear Path",
            font=("Comic Sans MS", 11, "bold"),
            bg="#f39c12",
            fg="black",
            activebackground="#e67e22",
            padx=20,
            pady=10,
            command=self.restart,
            cursor="hand2"
        )
        self.restart_btn.grid(row=0, column=2, padx=8)
        
        # Zoom controls
        zoom_frame = tk.Frame(button_frame, bg="#E8F4F8")
        zoom_frame.grid(row=0, column=3, padx=20)
        
        tk.Label(zoom_frame, text="🔍 Zoom:", font=("Arial", 10, "bold"), 
                bg="#E8F4F8", fg="#2c3e50").pack(side=tk.LEFT, padx=5)
        
        self.zoom_out_btn = tk.Button(
            zoom_frame,
            text="➖",
            font=("Arial", 12, "bold"),
            bg="#95a5a6",
            fg="black",
            width=3,
            command=self.zoom_out,
            cursor="hand2"
        )
        self.zoom_out_btn.pack(side=tk.LEFT, padx=2)
        
        self.zoom_label = tk.Label(
            zoom_frame,
            text="100%",
            font=("Arial", 10, "bold"),
            bg="#E8F4F8",
            fg="#2c3e50",
            width=6
        )
        self.zoom_label.pack(side=tk.LEFT, padx=5)
        
        self.zoom_in_btn = tk.Button(
            zoom_frame,
            text="➕",
            font=("Arial", 12, "bold"),
            bg="#95a5a6",
            fg="black",
            width=3,
            command=self.zoom_in,
            cursor="hand2"
        )
        self.zoom_in_btn.pack(side=tk.LEFT, padx=2)
        
        canvas_container = tk.Frame(self.frame, bg="#E8F4F8")
        canvas_container.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        
        deco_frame = tk.Frame(canvas_container, bg="#90C695", bd=10, relief=tk.RIDGE)
        deco_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas_frame = tk.Frame(deco_frame, bg="#5DADE2")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbars
        v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(
            canvas_frame,
            bg="#5DADE2",
            highlightthickness=0,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar.config(command=self.canvas.yview)
        h_scrollbar.config(command=self.canvas.xview)
        
        # Bind mouse wheel for zoom
        self.canvas.bind("<Control-MouseWheel>", self.on_mousewheel_zoom)
        
        legend_frame = tk.Frame(self.frame, bg="#E8F4F8")
        legend_frame.pack(pady=12)
        
        legend_border = tk.Frame(legend_frame, bg="#2E86AB", bd=3, relief=tk.RAISED)
        legend_border.pack()
        
        legend_inner = tk.Frame(legend_border, bg="white")
        legend_inner.pack(padx=10, pady=8)
        
        self.create_legend(legend_inner)
    
    def create_legend(self, parent):
        legend_items = [
            ("Baby Duck (Start)", "#FFD700"),
            ("Mother Duck (Goal)", "white"),
            ("Swimming Path", "#A8D8EA"),
            ("Reed Banks", "#7CB342"),
            ("Water", "#5DADE2")
        ]
        
        for i, (text, color) in enumerate(legend_items):
            frame = tk.Frame(parent, bg="white")
            frame.pack(side=tk.LEFT, padx=12)
            
            color_box = tk.Canvas(frame, width=22, height=22, bg=color, 
                                highlightthickness=2, highlightbackground="#2E86AB")
            color_box.pack(side=tk.LEFT, padx=5)
            
            label = tk.Label(frame, text=text, font=("Arial", 10, "bold"), 
                           bg="white", fg="#2c3e50")
            label.pack(side=tk.LEFT)
    
    def zoom_in(self):
        """Zoom in the maze"""
        if self.zoom_level < self.max_zoom:
            self.zoom_level = min(self.zoom_level + 0.2, self.max_zoom)
            self.update_zoom()
    
    def zoom_out(self):
        """Zoom out the maze"""
        if self.zoom_level > self.min_zoom:
            self.zoom_level = max(self.zoom_level - 0.2, self.min_zoom)
            self.update_zoom()
    
    def on_mousewheel_zoom(self, event):
        """Handle Ctrl+MouseWheel for zooming"""
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()
    
    def update_zoom(self):
        """Update the display with new zoom level"""
        self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")
        self.draw_maze()
        # Redraw path if exists
        if self.path_data and not self.animation_running:
            self.draw_complete_path()
    
    def load_maze(self, filename):
        try:
            # Dùng resource_path để tìm file
            file_path = resource_path(filename)
            print(f"[DEBUG] Loading maze from: {file_path}")
            
            with open(file_path, 'r') as f:
                lines = f.readlines()
                if not lines:
                    raise ValueError("Empty maze file")
                    
                first_line = lines[0].strip().split()
                if len(first_line) < 2:
                    raise ValueError("Invalid maze format")
                    
                self.rows = int(first_line[0])
                self.cols = int(first_line[1])
                
                self.maze_data = []
                self.has_entrance = False
                self.has_exit = False
                
                for i in range(1, min(self.rows + 1, len(lines))):
                    row_values = lines[i].strip().split()
                    row = []
                    for j in range(self.cols):
                        if j < len(row_values):
                            val = int(row_values[j])
                            row.append(val)
                            if val == 2:
                                self.has_entrance = True
                            elif val == 3:
                                self.has_exit = True
                        else:
                            row.append(1)
                    self.maze_data.append(row)
                    
                while len(self.maze_data) < self.rows:
                    self.maze_data.append([1] * self.cols)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load maze file: {str(e)}")
            self.maze_data = [[1] * 10 for _ in range(10)]
    
    def draw_maze(self):
        self.canvas.delete("all")
        
        if not self.maze_data:
            return
        
        # Calculate cell size with zoom
        base_cell_size = 40
        self.cell_size = int(base_cell_size * self.zoom_level)
        
        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size
        
        self.canvas.update_idletasks()
        canvas_actual_width = self.canvas.winfo_width()
        canvas_actual_height = self.canvas.winfo_height()
        
        self.offset_x = max(0, (canvas_actual_width - canvas_width) // 2)
        self.offset_y = max(0, (canvas_actual_height - canvas_height) // 2)
        
        self.canvas.config(scrollregion=(0, 0, max(canvas_width, canvas_actual_width), 
                                        max(canvas_height, canvas_actual_height)))
        
        # Draw maze cells
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_size + self.offset_x
                y1 = i * self.cell_size + self.offset_y
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                cell_value = self.maze_data[i][j]
                
                if cell_value == 1:
                    self.draw_pond_bank(x1, y1, x2, y2)
                elif cell_value == 2:
                    self.draw_water_with_lily(x1, y1, x2, y2)
                    # Don't draw baby duck here anymore - it will move
                elif cell_value == 3:
                    self.draw_water_with_lily(x1, y1, x2, y2)
                    self.draw_mother_swan(x1, y1, x2, y2)
                else:
                    self.draw_water_with_lily(x1, y1, x2, y2)
        
        # Draw baby duck at start position if not animating
        if not self.animation_running:
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.maze_data[i][j] == 2:
                        x1 = j * self.cell_size + self.offset_x
                        y1 = i * self.cell_size + self.offset_y
                        x2 = x1 + self.cell_size
                        y2 = y1 + self.cell_size
                        self.draw_baby_duck(x1, y1, x2, y2)
    
    def draw_pond_bank(self, x1, y1, x2, y2):
        """Draw pond banks with grass/reed texture"""
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#7CB342", outline="#689F38", width=2)
        
        num_lines = max(2, self.cell_size // 15)
        for i in range(num_lines):
            offset = i * (self.cell_size // num_lines)
            self.canvas.create_line(x1 + offset, y1, x1 + offset, y2, 
                                  fill="#558B2F", width=max(1, self.cell_size // 20))
    
    def draw_water_with_lily(self, x1, y1, x2, y2):
        """Draw water with subtle wave pattern"""
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#5DADE2", outline="#4A9BC7", width=1)
        
        mid_y = (y1 + y2) // 2
        self.canvas.create_line(x1, mid_y, x2, mid_y, fill="#81C9F0", width=1, smooth=True)
        
        import random
        if random.random() < 0.15:
            self.draw_lily_pad(x1, y1, x2, y2)
    
    def draw_lily_pad(self, x1, y1, x2, y2):
        """Draw a small lily pad"""
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        size = self.cell_size // 3
        
        self.canvas.create_oval(center_x - size//2, center_y - size//2, 
                              center_x + size//2, center_y + size//2,
                              fill="#7CB342", outline="#689F38", width=1)
        
        self.canvas.create_line(center_x + size//2, center_y, 
                              center_x + size//3, center_y,
                              fill="#689F38", width=2)
    
    def draw_baby_duck(self, x1, y1, x2, y2, tag="duck"):
        """Draw a cute baby duck"""
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        size = self.cell_size // 2
        
        # Duck body
        self.canvas.create_oval(center_x - size//2, center_y - size//3,
                              center_x + size//2, center_y + size//3,
                              fill="#FFD700", outline="#FFA500", width=max(1, size//10), tags=tag)
        
        # Duck head
        head_size = size // 2.5
        self.canvas.create_oval(center_x - head_size//2, center_y - size//2,
                              center_x + head_size//2, center_y - size//6,
                              fill="#FFD700", outline="#FFA500", width=max(1, size//10), tags=tag)
        
        # Duck beak
        self.canvas.create_polygon(
            center_x + head_size//2, center_y - size//3,
            center_x + head_size, center_y - size//3,
            center_x + head_size//2, center_y - size//4,
            fill="#FF8C00", outline="#FF6347", tags=tag
        )
        
        # Eye
        eye_size = max(2, size // 10)
        self.canvas.create_oval(center_x - eye_size//2, center_y - size//3,
                              center_x + eye_size//2, center_y - size//3 + eye_size,
                              fill="black", tags=tag)
    
    def draw_mother_swan(self, x1, y1, x2, y2):
        """Draw a mother swan/duck"""
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        size = self.cell_size // 1.8
        
        # Body
        self.canvas.create_oval(center_x - size//2, center_y - size//4,
                              center_x + size//2, center_y + size//3,
                              fill="white", outline="#CCCCCC", width=max(1, size//15))
        
        # Neck
        neck_points = [
            center_x - size//4, center_y - size//6,
            center_x - size//3, center_y - size//2,
            center_x - size//4, center_y - size//1.5
        ]
        self.canvas.create_line(neck_points, fill="white", width=max(4, size//5), smooth=True)
        self.canvas.create_line(neck_points, fill="#E0E0E0", width=max(3, size//6), smooth=True)
        
        # Head
        head_size = size // 3
        self.canvas.create_oval(center_x - size//3, center_y - size//1.4,
                              center_x - size//6, center_y - size//2,
                              fill="white", outline="#CCCCCC", width=max(1, size//15))
        
        # Beak
        self.canvas.create_polygon(
            center_x - size//3, center_y - size//1.5,
            center_x - size//2.2, center_y - size//1.5,
            center_x - size//3, center_y - size//1.7,
            fill="#FF8C00", outline="#FF6347"
        )
        
        # Eye
        eye_size = max(2, size // 10)
        self.canvas.create_oval(center_x - size//4, center_y - size//1.5,
                              center_x - size//5, center_y - size//1.7,
                              fill="black")
    
    def solve_maze(self):
        if not self.has_entrance:
            messagebox.showerror("🚫 Oops!", 
                "The maze is missing an entrance!\n"
                "The baby duckling can't start without a pond! 🦆")
            return
        if not self.has_exit:
            messagebox.showerror("🚫 Oh No!", 
                "Quack! The maze forgot to connect to Mom Duck!\n"
                "There's no exit for the duckling! 🦆💔")
            return

        try:
            # Tạo file temp_input.txt với đường dẫn ĐẦY ĐỦ của file maze
            maze_path = resource_path(self.selected_file)
            print(f"[DEBUG] Solving maze: {maze_path}")
            
            with open("temp_input.txt", "w") as f:
                f.write(maze_path)  # Ghi đường dẫn đầy đủ thay vì chỉ tên file
            
            exe_name = resource_path("main.exe") if os.name == 'nt' else resource_path("main")
            if not os.path.exists(exe_name.replace("./", "")):
                messagebox.showerror("🚫 Program Not Found", 
                    f"The rescue program '{exe_name}' is missing! 🦆\n\n"
                    f"Please compile your C++ code first using:\n"
                    f"g++ -o main main.cpp maze.cpp dijkstra.cpp")
                return
            
            with open("temp_input.txt", "r") as input_file:
                result = subprocess.run([exe_name], stdin=input_file, 
                                    capture_output=True, text=True, timeout=10)
            
            if os.path.exists("temp_input.txt"):
                os.remove("temp_input.txt")
            
            if result.returncode != 0:
                messagebox.showerror("✖ Program Error", 
                    f"The rescue program encountered an error:\n{result.stderr}\n\n"
                    f"The duckling is still waiting! 🦆")
                return
            
            if os.path.exists("path.txt") and os.path.getsize("path.txt") > 0:
                self.load_path()
                if self.path_data:
                    self.animate_duck_movement()
                else:
                    messagebox.showinfo("🚫 No Path Found", 
                        "The duckling is trapped! No path to Mom! 😢\n\n"
                        "Try a different maze or check the maze design.")
            else:
                messagebox.showinfo("🚫 No Solution", 
                    "No escape route found for the baby duckling!\n\n"
                    "The maze might be too tricky!")
                
        except subprocess.TimeoutExpired:
            messagebox.showerror("⏱ Timeout!", 
                "The rescue took too long! The program timed out.\n"
                "The maze might be too complex!")
        except Exception as e:
            messagebox.showerror("✖ Error", 
                f"Failed to solve maze: {str(e)}\n\n"
                f"The duckling is still waiting for rescue!")
    
    def load_path(self):
        try:
            self.path_data = []
            with open("path.txt", 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or not line.startswith("("):
                        continue
                    if line.endswith(")"):
                        coords = line[1:-1].split(",")
                        if len(coords) == 2:
                            x = int(coords[0])
                            y = int(coords[1])
                            self.path_data.append((x - 1, y - 1))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load path: {str(e)}")
            self.path_data = []
    
    def animate_duck_movement(self):
        """Animate the duck moving along the path"""
        self.animation_running = True
        self.current_step = 0
        self.solve_btn.config(state=tk.DISABLED)
        self.draw_maze()
        self.move_duck_step()
    
    def move_duck_step(self):
        """Move the duck one step along the path"""
        if not self.animation_running or not self.frame.winfo_exists():
            return

        if not self.path_data:
            self.animation_running = False
            if self.solve_btn.winfo_exists():
                self.solve_btn.config(state=tk.NORMAL)
            messagebox.showinfo("🚫 No Escape! 🦆", 
                "No escape for the baby duckling... the maze is too tricky!\n\n"
                "The duckling needs your help to find another way! 💔")
            return

        if self.current_step >= len(self.path_data):
            self.animation_running = False
            if self.solve_btn.winfo_exists():
                self.solve_btn.config(state=tk.NORMAL)

            actual_steps = len(self.path_data) - 1

            messagebox.showinfo("🎉 SUCCESS! 🎉", 
                f"Yay! The baby duckling is reunited with Mom! 💚\n\n"
                f"🏆 Path length: {actual_steps} steps\n"
                f"🌟 You're a true hero!")
            return
        
        row, col = self.path_data[self.current_step]
        
        # Draw path trail (not at start and end)
        if 0 <= row < len(self.maze_data) and 0 <= col < len(self.maze_data[0]):
            if 0 <= row < len(self.maze_data) and 0 <= col < len(self.maze_data[0]):
                x1 = col * self.cell_size + self.offset_x
                y1 = row * self.cell_size + self.offset_y
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Draw swimming trail
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#A8D8EA", 
                                            outline="#81C9F0", width=2, tags="path")
                if self.maze_data[row][col] == 3:
                    self.draw_mother_swan(x1, y1, x2, y2)
                # Add ripple effect
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                
                for i in range(1, 4):
                    radius = (self.cell_size // 6) * i
                    self.canvas.create_oval(center_x - radius, center_y - radius,
                                          center_x + radius, center_y + radius,
                                          outline="#B3E0F5", width=1, tags="path")
            
            # Draw duck at current position
            self.canvas.delete("duck")
            x1 = col * self.cell_size + self.offset_x
            y1 = row * self.cell_size + self.offset_y
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.draw_baby_duck(x1, y1, x2, y2, tag="duck")
        
        self.current_step += 1
        # Animation speed (100ms for smooth movement)
        self.root.after(100, self.move_duck_step)
    
    def draw_complete_path(self):
        """Draw the complete path without animation"""
        self.canvas.delete("path")
        for row, col in self.path_data:
            if 0 <= row < len(self.maze_data) and 0 <= col < len(self.maze_data[0]):
                if self.maze_data[row][col] != 2 and self.maze_data[row][col] != 3:
                    x1 = col * self.cell_size + self.offset_x
                    y1 = row * self.cell_size + self.offset_y
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#A8D8EA", 
                                                outline="#81C9F0", width=2, tags="path")
    
    def restart(self):
        """Clear the path and reset"""
        self.animation_running = False
        self.current_step = 0
        self.path_data = []
        self.draw_maze()
        self.solve_btn.config(state=tk.NORMAL if (self.has_entrance and self.has_exit) else tk.DISABLED)
        
        if os.path.exists("path.txt"):
            os.remove("path.txt")
    
    def back_to_selection(self):
        """Return to maze selection screen"""
        self.animation_running = False
        if os.path.exists("path.txt"):
            os.remove("path.txt")
        if os.path.exists("temp_input.txt"):
            os.remove("temp_input.txt")
        self.frame.destroy()
        show_selection_screen()
    
    def destroy(self):
        """Clean up resources"""
        self.animation_running = False
        self.frame.destroy()

def show_selection_screen():
    def on_select(filename):
        selection_screen.destroy()
        maze_ui = MazeUI(root, filename)
    
    selection_screen = MazeSelectionScreen(root, on_select)

# Main application
root = tk.Tk()
root.title("🦆 Duck Rescue - Maze Adventure 🦆")
root.geometry("1000x800")
root.configure(bg="#E8F4F8")

def on_select(filename):
    selection_screen.destroy()
    maze_ui = MazeUI(root, filename)

selection_screen = MazeSelectionScreen(root, on_select)

root.mainloop()