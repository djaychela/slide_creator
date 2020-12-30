from PIL import Image, ImageFont, ImageDraw
import pathlib

file_name = "q2020_test.txt"
current_dir = pathlib.Path(__file__).parent.absolute()
file_path = pathlib.Path(current_dir / "data" / file_name)

with open(file_path, "r") as file:
    slide_data = file.readlines()

q_text_colour = (255,255,255,255)
heading_colour = (255,255,255,190)
stroke_colour = (0,0,0,255)

image_file_name = "quiz_background_1610.jpg"
image_file_path = pathlib.Path(current_dir / "images" / image_file_name)

background = Image.open(image_file_path).convert("RGBA")

image_width = background.width

font_file_name = "Antonio-Bold.ttf"
font_file_path = pathlib.Path(current_dir / "fonts" / font_file_name)

round_fnt = ImageFont.truetype(str(font_file_path), 400)
round_title_fnt = ImageFont.truetype(str(font_file_path), 200)
fnt = ImageFont.truetype(str(font_file_path), 100)
q_fnt = ImageFont.truetype(str(font_file_path), 90)

idx = 0
finished = False
while not finished:
    question_content = []
    round, question = slide_data[idx].split()
    round_num = f"Round {round[1:]}"
    question_num = f"Question {question[1:]}"
    idx += 1
    while slide_data[idx].strip() != "":
        question_content.append(slide_data[idx].strip())
        idx +=1
    idx += 1
    print(round, question_num, question_content)
    if idx >= len(slide_data) - 1:
        finished = True

    if question[1:] != "0" and question[1:] != "x" and question[1:] != "t":
        # Standard Question Slide
        txt = Image.new("RGBA", background.size, (255,255,255,0))
        draw = ImageDraw.Draw(txt)

        round_width, _ = draw.textsize(round_num, font=fnt)
        draw.text(((image_width - round_width) / 2,10), round_num, font=fnt, fill=heading_colour, stroke_width=3, stroke_fill=stroke_colour)

        question_num_width, _ = draw.textsize(question_num, font=fnt)
        draw.text(((image_width - question_num_width) / 2,130), question_num, font=fnt, fill=heading_colour, stroke_width=3, stroke_fill=stroke_colour)

        content_length = len(question_content)
        content_y = 400

        for question_line in question_content:
            question_line_width, _ = draw.textsize(question_line, font=q_fnt)
            draw.text(((image_width - question_line_width) / 2,content_y), question_line, font=q_fnt, fill=q_text_colour, stroke_width=3, stroke_fill=stroke_colour)
            content_y += 120

    elif question[1:] == "0" or question[1:] == "x":
        # Round Start or End Slide
        txt = Image.new("RGBA", background.size, (255,255,255,0))
        draw = ImageDraw.Draw(txt)

        round_width, _ = draw.textsize(round_num, font=round_fnt)
        draw.text(((image_width - round_width) / 2,150), round_num, font=round_fnt, fill=heading_colour, stroke_width=10, stroke_fill=stroke_colour)

        round_title_width, _ = draw.textsize(question_content[0], font=round_title_fnt)
        draw.text(((image_width - round_title_width) / 2,700), question_content[0], font=round_title_fnt, fill=heading_colour, stroke_width=10, stroke_fill=stroke_colour)

    else:
        # Title Page
        txt = Image.new("RGBA", background.size, (255,255,255,0))
        draw = ImageDraw.Draw(txt)

        round_width, _ = draw.textsize(question_content[0], font=round_fnt)
        draw.text(((image_width - round_width) / 2,100), question_content[0], font=round_fnt, fill=heading_colour, stroke_width=10, stroke_fill=stroke_colour)

        round_title_width, _ = draw.textsize(question_content[1], font=round_fnt)
        draw.text(((image_width - round_title_width) / 2,550), question_content[1], font=round_fnt, fill=heading_colour, stroke_width=10, stroke_fill=stroke_colour)

    # output file to output folder
    output_file_name = f"R{round_num.split()[1]}Q{question_num.split()[1]}.jpg"
    output_file_path = pathlib.Path(current_dir / "output" / output_file_name)
    out = Image.alpha_composite(background, txt).convert("RGB")
    out.save(output_file_path, quality=95)

