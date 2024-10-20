import pdfplumber
import json
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import re
import os
from openai import OpenAI # required for compatibility with > v1.0.0
import time

# Access credentials
openai_apikey="REDACTED"
client = OpenAI(api_key=openai_apikey)

# function to extract text from a target PDF (not used in current iteration)
def extract_text_from_pdf(pdf_path):
    global global_tokens # global token counter
    global_tokens = 0
    global discipline # Chemical engineering, mathematics, medical
    global academic_level # Freshman, sophomore, junior, senior, masters, doctoral
    global class_name # Thermodynamics, calculus, anatomy
    global textbook_chunk_size
    global use_latest_model

    """Extract text from each page of the PDF."""
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # Adding a newline character after each page for better readability
    return text

def extract_text_with_ocr(pdf_path):
    text = ''
    with fitz.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf):
            # Attempt direct text extraction
            page_text = page.get_text()
            if page_text.strip():  # If there's text, append it
                text += page_text + "\n"
            else:  # If no text, attempt OCR
                pix = page.get_pixmap()
                img_bytes = pix.tobytes("png")  # Convert the page to an image
                img = Image.open(io.BytesIO(img_bytes))
                page_text = pytesseract.image_to_string(img)
                text += page_text + "\n"
    return text


# modelled on assistant_openai_xcode.py (as of 5 Feb 24) + JSON output mode
def generate_qa_pairs(text_chunk, use_latest_model): 
    global global_tokens # global token counter
    global_tokens = 0
    global discipline # Chemical engineering, mathematics, medical
    global academic_level # Freshman, sophomore, junior, senior, masters, doctoral
    global class_name # Thermodynamics, calculus, anatomy
    global textbook_chunk_size
    
    model = "gpt-4-turbo-preview" if use_latest_model else "gpt-3.5-turbo-0125"
    

    try:
        response = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            seed = 36, # note seed of '36' must ALWAYS BE USED across ALL project outputs
            temperature = 0.25,
            messages=[
                {
                    "role": "system",
                    "content": """
                                            You are a university teaching assistant in for a class in '{class_name}' in the discipline of '{discipline}', who has been tasked with generating three technical question-answer-reference triplet for the Professor based on the text provided in their message. For each question-answer-reference triplet, structure your response in JSON format. Each json JSON object should contain a 'question#' field followed by the question text, an 'answer#' field for the answer text, and a 'references#' field for the references text, all of which must be consistent with the information provided in the text passage below.


                        Given the technical text provided, generate a dataset entry consisting of triplets of a question, a response, and relevant references. Follow these guidelines for each component:

                        Question:
                        - Objective: Craft a question that a '{academic_level}' level student in '{discipline}' student might ask after reading the text. The question should reflect the diversity of student backgrounds, acknowledging the varied cultural, geographic, and educational contexts from which they come.
                        - Considerations: Ensure the question is clear, focused, and directly related to the technical content of the provided text. The question should invite a response that clarifies, expands upon, or applies the text's information.
                        
                        Response:
                        - Objective: Write a response in the style a professor might use to reply to a '{academic_level}' level student's question. The response should aim to be between 50 and 100 words, technically accurate, and comprehensible to students at a '{academic_level}' level.
                        - Considerations: Utilize simplifying metaphors or similes where appropriate to aid understanding. The response should educate and clarify, enhancing the student's grasp of the subject matter without oversimplifying the technical complexity.
                        
                        References:
                        - Objective: Provide concise technical sentences relevant to the question's topic. These sentences should contain technically accurate information that a professor would likely reference to formulate their response.
                        - Considerations: The references should be directly related to both the question and response, offering a foundation for further exploration or verification of the information presented.
                    

                        Since must generate THREE question-answer-reference triplets in JSON output, which must correspond to the following nine entries in the json output structure: 

                        '{"question1": "Text generated for question 1.", "answer1": "Text generated for answer 1.", "references1": "Text generated for refrences 1", "question2": "Text generated for question 2.", "answer2": "Text generated for answer 2.", "references2": "Text generated for references 3.", "question3": "Text generated for question 3.", "answer3": "Text generated for answer 3.", "references3": "Text generated for references 3."}'

                    """
                },
                {
                    "role": "user",
                    "content": f"""

                        Thank you for your help with this task. Our goal is to generate technical question and answer pairs for a '{academic_level}' level student studying a class in '{class_name}' within the discipline of '{discipline}' at a prestigious university. To ensure the technical accuracy of these questions, please base the technical answers only on the technically accurate, relevant to '{class_name}' and informed on content based in the passage. 

                        Based on the content, context, and complexities of the provided text, create a dataset entry with the following components:
                        - A question reflective of the inquiries of a '{academic_level}' level student in a class on '{class_name}' within the disciplien of '{discipline}'.
                        - A professorial response to that question, adhering to the specified word limit and stylistic guidelines.
                        - A set of references that provide succinct, concise technical information relevant to the question and answer and suitable for a university class in '{class_name}'.
                        Remember, the goal is to facilitate understanding, encourage critical thinking, and support the educational development of '{discipline}' students across a wide range of backgrounds.
                        
                        ***BEGIN PASSAGE***

                        '{text_chunk}' 
                        
                        ***END PASSAGE***

                        If the passage contains no information relevant to the discipline of '{discipline}' or the broad subject of '{class_name}', please respond with "NOCONTENT" for all three fields in the triple: "Text generated for question #" , "Text generated for answer #" , and "Text generated for references #".

                        If the passage does contain information relevant to the discipline of '{discipline}' AND the broad subject of '{class_name}', please generate three question-answer-reference triplets: nine (9) entries total, which must be output in json (JSON) format. 

                        Now, pelase respond in the json format specified, with three question-answer-reference triplets.
                    """
                }
            ] # close Message object        
        ) # close response definition
        tokens_used = response.usage.total_tokens
        global_tokens += tokens_used

    except Exception as oops:
        print (f"Q-A generation failure: {oops}")
        time.sleep(3)
    try: # extract response content
        qa_content = json.loads(response.choices[0].message.content)  # assuming JSON format
        formatted_qa_pairs = [] # clear temp JSON entries

        # Loop through the three Q&A pairs
        for i in range(1, 4):
            question_key = f"question{i}"
            answer_key = f"answer{i}"
            references_key = f"references{i}"

            question = qa_content.get(question_key, "NOCONTENT")
            answer = qa_content.get(answer_key, "NOCONTENT")
            references = qa_content.get(references_key, "NOCONTENT")

            if question == "NOCONTENT" or answer == "NOCONTENT" or references == "NOCONTENT":
                continue  # Skip this pair

            formatted_text = f"### Query: {question} ### Response: {answer} ### References: {references} ###"
            formatted_qa_pairs.append({"text": formatted_text})
        return formatted_qa_pairs
    except Exception as e: # associated only with JSON format/object parse
        print(f"An error occurred while processing the Q&A pairs: {e}")
        return []

def segment_text_and_generate_dataset(submitted_text, submitted_chunk_size, use_latest_model):
    global global_tokens # global token counter
    global_tokens = 0
    global discipline # Chemical engineering, mathematics, medical
    global academic_level # Freshman, sophomore, junior, senior, masters, doctoral
    global class_name # Thermodynamics, calculus, anatomy
    global textbook_chunk_size

    # Split the text into chunks of approximately chunk_size words
    words = submitted_text.split()
    chunks = [' '.join(words[i:i+submitted_chunk_size]) for i in range(0, len(words), submitted_chunk_size)]
    
    # Initialise local dataset variable and assign chunks
    dataset = []

    total_questions = 3*len(chunks)  # 3 questions per chunk

    # chunk size bounded by second passed variable
    for chunk in chunks:
        # pass resultant chunk to QA_pair function
        qa_pairs = generate_qa_pairs(chunk, use_latest_model)
        # append resultant QA pairs to dataset
        for pair in qa_pairs:
            dataset.append(pair)
        print(f"Processed {len(dataset)} of {total_questions} questions processed.")
    # return JSON dataset containing Q&A pairs for all segments of the text
    return dataset

def post_process_ocr_text(text):
    # Add spaces before all capital letters that are not preceded by a space or start of a line
    text = re.sub(r"(?<!^)(?<! )([A-Z])", r" \1", text)
    
    # Attempt to add line breaks by detecting patterns, e.g., end of sentences followed by a capital letter without a break
    text = re.sub(r"(\.)([A-Z])", r"\1\n\2", text)
    
    # This is a simplistic approach and might need refinement based on actual text patterns and layout
    
    return text


def main():
    global global_tokens # global token counter
    global_tokens = 0
    global discipline # Chemical engineering, mathematics, medical
    global academic_level # Freshman, sophomore, junior, senior, masters, doctoral
    global class_name # Thermodynamics, calculus, anatomy
    global textbook_chunk_size
    global use_latest_model
    global target_filename
    global target_dir_path

    if target_filename.endswith(".pdf"):

        # Construct the full path to the PDF file
        pdf_path = os.path.join(target_dir_path, target_filename)
        
        # Extract text from the current PDF file
        target_content = extract_text_from_pdf(pdf_path)

        if len(target_content) < 10000: # proper text extraction failed
            print(f"Text export failed for {target_filename}. Attempting OCR.")
            target_content = extract_text_with_ocr(pdf_path)
            target_content = post_process_ocr_text(target_content)

        
        dataset = segment_text_and_generate_dataset(target_content, textbook_chunk_size, use_latest_model)

        output_filename = target_filename.replace('.pdf', '_Training.jsonl')
        output_path = os.path.join(target_dir_path, output_filename)

        # Dump the target training dataset to JSONL file within the same directory as the PDFs
        with open(output_path, 'w') as outfile:
            for entry in dataset:
                json.dump(entry, outfile)
                outfile.write('\n')
                
        print(f"Training data extraction completed for {target_filename}.")

    else: # Default to single text file
        # follow previous pathway of analysing single .txt file resource in target by name
        # *************************************

        # Read target file
        textbook_path = os.path.join(target_dir_path, target_filename)
        with open(textbook_path, 'r') as textbook_file:
            textbook_content = textbook_file.read()
            
        # Segment the text and generate Q&A pairs (nested function) for each segment
        dataset = segment_text_and_generate_dataset(textbook_content, textbook_chunk_size, use_latest_model)
        
        # Saving the dataset in the required JSON format
        output_filename = target_filename.replace('.txt', '_Training.jsonl')
        output_path = os.path.join(os.path.dirname(__file__), output_filename)
        # Dump target training dataset to JSONL file within working directory (not resource directory)
        with open(output_path, 'w') as outfile:
            for entry in dataset:
                json.dump(entry, outfile)
                outfile.write('\n')


    

if __name__ == '__main__':
    global global_tokens # global token counter
    global_tokens = 0
    global discipline # Chemical engineering, mathematics, medical
    global academic_level # Freshman, sophomore, junior, senior, masters, doctoral
    global class_name # Thermodynamics, calculus, anatomy
    global textbook_chunk_size
    global use_latest_model
    global target_filename
    global target_dir_path

    discipline = "Chemical Engineering" #Medicine, Education, Chemical Engineering
    academic_level = "Undergraduate Engineering" #Doctoral MD, Masters
    class_name = "Unit Operations" #All Medical Subjects, Tertiary Assessment, Thermodynamics
    textbook_chunk_size = 250 # NOTE: USER VAR (GPT-4-turbo/latest = 128k token max)
    use_latest_model = True # NOTE: USER VAR (False -> gpt-3.5-turbo-0125 w/16.385k token max)
    target_dir_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'unitops_books')
    target_filename = 'unitops2021lectures.pdf' 


    main()

    print("Training data extraction completed.")
    print(f"Total tokens used: {global_tokens}")