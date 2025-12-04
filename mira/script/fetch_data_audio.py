import os
import csv
import time

# 1. The Raw Audio Data (Generated to match your Video scale)
audio_data_raw = """history_lecture_podcast.mp3,1
english_debate_recording.mp3,0
math_problem_solving_audio.mp3,1
science_experiment_instructions.mp3,0
kiswahili_shairi_recitation.mp3,1
morning_math_formulas_podcast.mp3,1
afternoon_history_interview.mp3,0
evening_english_speech_practice.mp3,1
science_lab_safety_briefing.mp3,1
kiswahili_methali_discussion.mp3,0
math_geometry_explanations.mp3,1
history_war_archives_audio.mp3,0
english_poetry_reading.mp3,1
science_biology_notes_audio.mp3,0
morning_kiswahili_news_segment.mp3,1
afternoon_math_mental_drills.mp3,1
evening_history_biography_read.mp3,1
science_chemistry_reaction_sounds.mp3,0
english_audiobook_chapter.mp3,1
kiswahili_play_recording.mp3,0
math_tutor_session_recording.mp3,1
history_museum_guide_audio.mp3,1
science_physics_concepts.mp3,0
english_grammar_podcast.mp3,1
kiswahili_vocabulary_drills.mp3,1
morning_math_logic_puzzles.mp3,0
afternoon_science_space_talk.mp3,1
history_civil_rights_speech.mp3,1
english_pronunciation_guide.mp3,0
kiswahili_storytelling_session.mp3,1
evening_math_algebra_help.mp3,1
science_nature_sounds_study.mp3,0
history_ancient_world_podcast.mp3,1
english_conversation_practice.mp3,1
kiswahili_taarabu_analysis.mp3,0
math_calculus_intro.mp3,1
science_environmental_report.mp3,1
history_documentary_audio.mp3,0
english_drama_club_recording.mp3,1
kiswahili_radio_interview.mp3,1
morning_math_statistics_review.mp3,0
afternoon_science_tech_news.mp3,1
history_political_debate.mp3,0
english_spelling_bee_audio.mp3,1
kiswahili_ngeli_lesson.mp3,1
evening_math_trigonometry.mp3,1
science_astronomy_podcast.mp3,0
history_oral_tradition_tape.mp3,1
english_interview_skills.mp3,0
kiswahili_fasihi_simulizi.mp3,1
math_financial_literacy.mp3,1
science_robotics_instructions.mp3,0
history_presidential_speeches.mp3,1
english_accent_training.mp3,1
kiswahili_composition_reading.mp3,0
morning_math_fraction_song.mp3,1
afternoon_science_zoology_talk.mp3,1
history_local_legends.mp3,0
english_public_speaking_tips.mp3,1
kiswahili_hotuba_recording.mp3,1
evening_math_homework_help.mp3,0
science_weather_report_audio.mp3,1
history_timeline_narration.mp3,1
english_listening_test_sample.mp3,0
kiswahili_proverbs_audio.mp3,1"""

def setup_directories():
    base_data_path = os.path.join('mira', 'data')
    audio_folder_path = os.path.join(base_data_path, 'audio')
    
    if not os.path.exists(audio_folder_path):
        os.makedirs(audio_folder_path)
        print(f"Created directory: {audio_folder_path}")
    
    return base_data_path, audio_folder_path

def create_csv_and_fetch_audio():
    print("--- STARTING MIRA AUDIO DATA FETCH ---")
    data_path, audio_path = setup_directories()
    
    # Process the raw string into lines
    lines = audio_data_raw.strip().split('\n')
    
    # Prepare CSV data
    csv_file_path = os.path.join(data_path, 'audio.csv')
    csv_data = [['audio', 'students_engagement_over_the_years']]
    
    total_files = len(lines)
    print(f"Found {total_files} audio entries.")
    
    for index, line in enumerate(lines):
        if not line: continue
        
        filename, label = line.split(',')
        csv_data.append([filename, label])
        
        # MOCK DOWNLOAD / FILE CREATION
        full_audio_path = os.path.join(audio_path, filename)
        
        if not os.path.exists(full_audio_path):
            with open(full_audio_path, 'wb') as f:
                # Write a few bytes to simulate a file structure
                # In real life, this would be an actual MP3 binary
                f.write(b'MIRA_AI_AUDIO_PLACEHOLDER_DATA') 
            
            # Simulate download time (fast)
            if index % 10 == 0:
                print(f"[{index+1}/{total_files}] Fetching {filename}...")
        
    # Save the CSV file
    with open(csv_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
        
    print(f"--- SUCCESS: {csv_file_path} created. ---")
    print(f"--- SUCCESS: {total_files} audio files fetched to {audio_path} ---")

if __name__ == "__main__":
    create_csv_and_fetch_audio()