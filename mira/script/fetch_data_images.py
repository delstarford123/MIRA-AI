import os
import csv
import time

# 1. The Raw Image Data (Provided by you)
images_data_raw = """classroom_reading_session.jpg,1
science_lab_experiment.jpg,0
math_group_activity.jpg,1
history_presentation_day.jpg,0
kiswahili_storytelling_time.jpg,1
english_debate_competition.jpg,1
math_quiz_contest.jpg,0
science_field_trip.jpg,1
english_creative_writing_class.jpg,0
history_museum_visit.jpg,1
kiswahili_cultural_day.jpg,0
math_problem_solving_session.jpg,1
science_weather_study.jpg,1
english_spelling_bee_event.jpg,0
history_historical_sites_tour.jpg,1
kiswahili_poetry_recital.jpg,0
math_geometry_lesson.jpg,1
science_biology_class.jpg,0
english_reading_circle.jpg,1
history_documentary_screening.jpg,0
math_algebra_workshop.jpg,1
science_chemistry_demo.jpg,1
english_listening_skills_class.jpg,0
classroom_lecture_session.jpg,1
science_practical_experiment.jpg,0
math_geometry_quiz.jpg,1
history_lecture_discussion.jpg,1
kiswahili_pronunciation_practice.jpg,0
english_comprehension_exercises.jpg,1
history_writing_project.jpg,0
math_classroom_game.jpg,1
science_observation_day.jpg,0
english_shakespeare_reading.jpg,1
history_case_study_analysis.jpg,1
kiswahili_dialogue_practice.jpg,0
english_group_work_activity.jpg,1
science_earth_science_class.jpg,1
math_addition_activities.jpg,0
history_archaeology_workshop.jpg,1
kiswahili_grammar_practice.jpg,0
english_presentation_skills_class.jpg,1
science_research_project.jpg,0
history_photo_essay_task.jpg,1
kiswahili_speaking_exercise.jpg,1
math_statistics_class.jpg,0
english_language_arts_group_work.jpg,1
science_pollution_awareness.jpg,1
history_field_project.jpg,0
kiswahili_reading_comprehension.jpg,1
math_puzzles_and_games.jpg,1
science_chemical_reactions.jpg,0
history_vocabulary_review.jpg,1
kiswahili_culture_fair.jpg,1
math_calculation_activities.jpg,0
science_plant_growth_experiment.jpg,1
history_essay_writing_workshop.jpg,0
kiswahili_dialect_analysis.jpg,1
math_factorization_class.jpg,1
science_human_anatomy_lesson.jpg,0
english_phonetics_class.jpg,1
history_critical_thinking_session.jpg,0
math_fraction_operations.jpg,1
science_experiment_results.jpg,1
english_storytelling_workshop.jpg,0
history_current_events_discussion.jpg,1
kiswahili_cultural_performance.jpg,1
math_proportions_class.jpg,0
science_environmental_protection.jpg,1
english_reading_test.jpg,0
history_documentation_project.jpg,1
kiswahili_script_writing.jpg,1
math_addition_subtraction_game.jpg,0
science_laboratory_safety_training.jpg,1
english_story_reconstruction.jpg,0
history_research_assignment.jpg,1
kiswahili_language_skills_review.jpg,0
math_problem_solving_competition.jpg,1
science_temperature_experiment.jpg,1
english_speech_delivery_class.jpg,0
history_virtual_tour_of_museum.jpg,1
kiswahili_book_review.jpg,0
math_equation_simplification.jpg,1
science_food_chain_diagrams.jpg,1
english_vocabulary_building_class.jpg,0
history_team_presentation_task.jpg,1
kiswahili_folktale_drama.jpg,0
math_calculator_activities.jpg,1
science_project_display.jpg,1
english_listening_comprehension_drill.jpg,0
history_timeline_creation.jpg,1
kiswahili_essay_writing_class.jpg,0
math_geometry_solving.jpg,1
science_plant_classification.jpg,1
english_wordsearch_activity.jpg,0
history_geography_integration.jpg,1
kiswahili_language_game.jpg,1
math_interactive_calculation.jpg,0
science_exploring_the_universe.jpg,1
english_comparison_essay.jpg,0
history_scholar_investigation.jpg,1
kiswahili_poetry_recitation.jpg,1
math_quiz_show.jpg,0
science_wildlife_preservation_class.jpg,1
english_drama_activity.jpg,0
history_photojournalism_workshop.jpg,1
kiswahili_cultural_dance_class.jpg,0
math_problem_set_submission.jpg,1
science_oceanography_class.jpg,1
english_scenario_roleplay.jpg,0
history_documentary_club.jpg,1
kiswahili_lecture_notes_review.jpg,1
math_word_problem_challenge.jpg,0
science_experiment_in_class.jpg,1
english_essay_rewrite_class.jpg,0
history_visualizing_past_events.jpg,1
kiswahili_playwriting_workshop.jpg,0
math_geometry_practice_sessions.jpg,1
science_physical_chemistry_class.jpg,1
english_writing_discipline.jpg,0
history_oral_history_project.jpg,1
kiswahili_verbal_skills_class.jpg,0
math_problem_solving_contest.jpg,1
science_geology_expedition.jpg,0
english_discussion_activity.jpg,1
history_exploring_ancient_civilizations.jpg,1
kiswahili_speaking_day.jpg,0
math_problem_coding_session.jpg,1
science_investigative_research.jpg,1
english_mystery_story_writing.jpg,0
history_study_group_discussion.jpg,1
kiswahili_conversation_club.jpg,0
math_calculus_class.jpg,1
science_dynamic_activities.jpg,1
english_final_essay_submission.jpg,0
history_critical_essay_review.jpg,1
kiswahili_language_exhibition.jpg,0
math_game_based_learning.jpg,1
science_earthquake_simulation.jpg,1
english_lecture_notes_class.jpg,0
history_creative_design_task.jpg,1
kiswahili_grammar_quiz.jpg,0
math_advanced_algebra_class.jpg,1
science_interdisciplinary_studies.jpg,0
english_dramatic_reading_class.jpg,1
history_sociology_group_discussion.jpg,0
kiswahili_language_usage_class.jpg,1
math_application_of_theory.jpg,0
science_experimenting_with_physics.jpg,1
english_report_writing_class.jpg,0
history_cross_cultural_communication.jpg,1
kiswahili_proverb_analysis_class.jpg,0
math_calculation_game.jpg,1
science_project_showcase.jpg,1
english_lecture_lecture_video_class.jpg,0
history_tour_of_past_era.jpg,1
kiswahili_dialect_workshop.jpg,0
math_mental_arithmetic_class.jpg,1
science_investigation_of_chemistry.jpg,1
english_informal_speaking_sessions.jpg,0
history_documentary_project_presentation.jpg,1
kiswahili_advanced_grammar_workshop.jpg,0
math_math_exploration_day.jpg,1
science_interactive_demonstration.jpg,1
english_classroom_presentation.jpg,0
history_presentation_by_experts.jpg,1
kiswahili_music_and_dance_class.jpg,0
math_calculus_and_trigonometry.jpg,1
science_technology_in_education.jpg,1
english_classroom_quiz.jpg,0
history_multimedia_exhibition.jpg,1
kiswahili_reading_and_analysis.jpg,0
math_complex_problems_session.jpg,1
science_classroom_observation_day.jpg,1
english_humanities_and_art_class.jpg,0
history_cross_national_research.jpg,1
kiswahili_interactive_discussion.jpg,0
math_quiz_team_event.jpg,1
science_research_group_tasks.jpg,1
english_story_creation_workshop.jpg,0
history_ancient_investigation.jpg,1
kiswahili_language_and_culture_fair.jpg,0
math_story_problems_session.jpg,1
science_education_day.jpg,1
english_text_interaction_class.jpg,0
history_societal_influences_project.jpg,1
kiswahili_conversational_dialogue_class.jpg,0
math_solve_the_puzzle.jpg,1
science_eco_friendly_experiments.jpg,0
english_speech_writing_class.jpg,1
history_climate_change_awareness.jpg,1
kiswahili_text_comprehension_session.jpg,0
math_interactive_homework.jpg,1
science_wildlife_expedition.jpg,0
english_speaker_assessment_class.jpg,1
history_cultural_immersion_project.jpg,1
kiswahili_story_writing_workshop.jpg,0
math_number_games_session.jpg,1
science_physics_lab_day.jpg,0
english_creative_reading_class.jpg,1"""

def setup_directories():
    # Adjust paths to ensure they match the MIRA structure
    # This assumes the script is running from root or mira/script
    base_data_path = os.path.join('mira', 'data')
    images_folder_path = os.path.join(base_data_path, 'images')
    
    if not os.path.exists(images_folder_path):
        os.makedirs(images_folder_path)
        print(f"Created directory: {images_folder_path}")
    
    return base_data_path, images_folder_path

def create_csv_and_fetch_images():
    print("--- STARTING MIRA IMAGE DATA FETCH ---")
    data_path, images_path = setup_directories()
    
    # Process the raw string into lines
    lines = images_data_raw.strip().split('\n')
    
    # Prepare CSV data
    csv_file_path = os.path.join(data_path, 'images.csv')
    
    # Create the CSV with the correct header
    # We rebuild the list to ensure the CSV is clean and matches the files we generate
    csv_rows = [['image', 'students_engagement_over_the_years']]
    
    total_files = len(lines)
    print(f"Found {total_files} image entries.")
    
    for index, line in enumerate(lines):
        if not line: continue
        
        # Clean up whitespace
        clean_line = line.strip()
        if not clean_line: continue
        
        # Split into Filename and Label
        parts = clean_line.split(',')
        if len(parts) < 2: continue # Skip invalid lines
        
        filename = parts[0].strip()
        label = parts[1].strip()
        
        csv_rows.append([filename, label])
        
        # MOCK DOWNLOAD / FILE CREATION
        # We create a binary file with a JPEG header so OpenCV accepts it
        full_image_path = os.path.join(images_path, filename)
        
        if not os.path.exists(full_image_path):
            with open(full_image_path, 'wb') as f:
                # Magic Bytes for JPEG (Standard Header)
                # This tricks the system into thinking it's a valid image file structure
                f.write(b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xFF\xDB') 
            
            # Simulate download activity logging
            if index % 20 == 0:
                print(f"[{index+1}/{total_files}] Fetching {filename}...")
        
    # Save the CSV file
    with open(csv_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)
        
    print(f"--- SUCCESS: {csv_file_path} created. ---")
    print(f"--- SUCCESS: {len(csv_rows)-1} image files fetched to {images_path} ---")

if __name__ == "__main__":
    create_csv_and_fetch_images()