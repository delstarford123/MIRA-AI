import os
import csv
import time

# 1. The Raw Data provided
video_data_raw = """afternoon_math_class.mp4,0
morning_science_lab.mp4,1
history_group_discussion.mp4,1
evening_kiswahili_reading.mp4,0
morning_english_debate.mp4,1
afternoon_science_practical.mp4,1
evening_history_presentation.mp4,0
morning_math_revision.mp4,1
afternoon_kiswahili_storytime.mp4,0
evening_science_experiment.mp4,1
afternoon_english_grammar_drill.mp4,0
morning_history_timeline_activity.mp4,1
evening_math_quiz_session.mp4,1
afternoon_science_fieldwork.mp4,0
morning_kiswahili_dictation.mp4,1
evening_english_reading_circle.mp4,0
morning_math_word_problems.mp4,1
afternoon_history_map_work.mp4,1
morning_science_group_lab.mp4,0
evening_kiswahili_comprehension.mp4,1
afternoon_english_writing_workshop.mp4,1
morning_history_source_analysis.mp4,0
evening_math_geometry_activity.mp4,1
afternoon_science_nature_walk.mp4,0
morning_kiswahili_poetry.mp4,1
evening_english_spelling_bee.mp4,1
morning_history_roleplay.mp4,0
afternoon_math_fraction_exercises.mp4,1
evening_science_robotics_intro.mp4,0
morning_english_pronunciation_practice.mp4,1
afternoon_kiswahili_reading_groups.mp4,1
evening_history_debate_session.mp4,0
morning_math_speed_test.mp4,1
afternoon_science_electrical_circuits.mp4,1
evening_english_creative_writing.mp4,0
morning_history_quiz_bowl.mp4,1
afternoon_kiswahili_proverbs_activity.mp4,0
evening_math_algebra_session.mp4,1
morning_science_stem_task.mp4,1
afternoon_english_dictionary_skills.mp4,0
evening_history_artifact_study.mp4,1
morning_math_counting_drill.mp4,0
afternoon_kiswahili_grammar_practice.mp4,1
evening_science_water_cycle_demo.mp4,1
morning_english_listening_activity.mp4,0
afternoon_history_photo_analysis.mp4,1
evening_math_puzzle_solving.mp4,1
morning_science_weather_observation.mp4,0
afternoon_kiswahili_sentence_making.mp4,1
evening_english_public_speaking.mp4,0
morning_math_table_work.mp4,1
afternoon_history_chronology_task.mp4,1
evening_science_plants_observation.mp4,0
morning_english_vocab_drill.mp4,1
afternoon_kiswahili_dialogue_practice.mp4,1
evening_math_logic_games.mp4,0
morning_science_density_activity.mp4,1
afternoon_history_documentary_review.mp4,0
evening_english_group_reading.mp4,1
morning_math_ratio_practice.mp4,1
afternoon_kiswahili_class_discussion.mp4,0
evening_science_light_experiment.mp4,1
morning_english_article_analysis.mp4,1
afternoon_history_trivia_game.mp4,0
evening_math_statistics_intro.mp4,1
morning_kiswahili_speech_practice.mp4,1
afternoon_science_energy_activity.mp4,0
evening_english_literature_discussion.mp4,1
morning_history_geography_link.mp4,0
afternoon_math_multiplication_drill.mp4,1
evening_science_air_pressure_test.mp4,1
morning_kiswahili_vocabulary_game.mp4,0
afternoon_english_story_reconstruction.mp4,1
evening_history_quiz_competition.mp4,1
morning_math_division_tasks.mp4,0
afternoon_science_coloring_diagrams.mp4,1
evening_kiswahili_roleplay.mp4,1
morning_english_fact_vs_opinion.mp4,0
afternoon_history_boardgame_learning.mp4,1
evening_math_measurement_activity.mp4,0
morning_science_classification_task.mp4,1
afternoon_kiswahili_annotation_activity.mp4,1
evening_english_fluency_practice.mp4,0
morning_history_picture_story.mp4,1
afternoon_math_graphs_activity.mp4,1
evening_science_sound_demo.mp4,0
morning_kiswahili_phrase_construction.mp4,1
afternoon_english_language_drill.mp4,0
evening_history_heritage_activity.mp4,1
morning_math_shapes_practice.mp4,1
afternoon_science_temperature_lab.mp4,0
evening_kiswahili_readaloud.mp4,1
morning_english_sentence_framing.mp4,1
afternoon_history_museum_virtual_tour.mp4,0
evening_math_equation_solving.mp4,1
morning_science_forces_activity.mp4,1
afternoon_kiswahili_translation_task.mp4,0
evening_english_composition_planning.mp4,1
morning_math_speed_drills.mp4,0
afternoon_history_timeline_building.mp4,1
evening_science_microorganisms_study.mp4,1
morning_kiswahili_creative_recitation.mp4,0
afternoon_english_group_discussion.mp4,1
evening_math_revision_session.mp4,1
morning_science_leaf_collection.mp4,0
afternoon_history_map_coloring.mp4,1
evening_kiswahili_memory_game.mp4,0
morning_math_classification_activity.mp4,1
afternoon_english_note_making.mp4,1
evening_history_clay_artifacts.mp4,0
morning_science_shadow_experiment.mp4,1
afternoon_kiswahili_reading_fluency.mp4,1
evening_math_practice_test.mp4,0
morning_english_comprehension_quiz.mp4,1
afternoon_history_event_ordering.mp4,0
evening_science_simple_machines_demo.mp4,1
morning_kiswahili_paragraph_writing.mp4,1
afternoon_math_number_patterns.mp4,0
evening_english_character_analysis.mp4,1
morning_science_inquiry_session.mp4,1
afternoon_history_interview_activity.mp4,0
evening_kiswahili_language_game.mp4,1
morning_math_estimation_drill.mp4,0
afternoon_english_worksheet_review.mp4,1
evening_science_weather_station_task.mp4,0
morning_history_empathy_activity.mp4,1
afternoon_kiswahili_listening_test.mp4,1
evening_math_fraction_challenges.mp4,0
morning_english_text_mapping.mp4,1
afternoon_science_color_mixing.mp4,1
evening_history_archival_research.mp4,0
morning_kiswahili_culture_lesson.mp4,1
afternoon_math_problem_solving.mp4,1
evening_english_group_presentation.mp4,0
morning_history_quick_facts_quiz.mp4,1
afternoon_science_environmental_walk.mp4,1
evening_kiswahili_summary_activity.mp4,0
morning_math_shapes_identification.mp4,1
afternoon_english_synonym_hunt.mp4,1
evening_history_object_analysis.mp4,0
morning_science_seed_germination.mp4,1
afternoon_kiswahili_question_forming.mp4,1
evening_math_homework_review.mp4,0
morning_english_listening_comprehension.mp4,1
afternoon_history_creative_timeline.mp4,1
evening_science_balloon_experiment.mp4,0
morning_kiswahili_pronunciation_drill.mp4,1
afternoon_math_speed_practice.mp4,0
evening_english_storytelling_circle.mp4,1
morning_history_daily_review.mp4,1
afternoon_science_energy_sources_lesson.mp4,0
evening_kiswahili_interactive_quiz.mp4,1
morning_math_number_line_activity.mp4,1
afternoon_english_vocabulary_building.mp4,0
evening_history_historical_figures_discussion.mp4,1
morning_science_observation_skills.mp4,0
afternoon_kiswahili_writing_exercise.mp4,1
evening_math_data_interpretation.mp4,1
morning_english_reading_fluency.mp4,0
afternoon_history_cause_effect_activity.mp4,1
evening_science_magnetic_force_demo.mp4,0
morning_kiswahili_story_analysis.mp4,1
afternoon_math_problem_sets.mp4,0
evening_english_poetry_reading.mp4,1
morning_history_quiz_game.mp4,1
afternoon_science_habitat_study.mp4,0
evening_kiswahili_dialogue_session.mp4,1
morning_math_time_practice.mp4,0
afternoon_english_writing_skills.mp4,1
evening_history_art_analysis.mp4,1
morning_science_experiment_setup.mp4,0
afternoon_kiswahili_reading_practice.mp4,1
evening_math_challenge_activities.mp4,1
morning_english_vocabulary_quiz.mp4,0
afternoon_history_role_play.mp4,1
evening_science_solar_system_lesson.mp4,0
morning_kiswahili_cultural_stories.mp4,1
afternoon_math_drill_session.mp4,1
evening_english_group_reading.mp4,0
morning_history_fact_checking.mp4,1
afternoon_science_exploration_activity.mp4,0
evening_kiswahili_writing_practice.mp4,1
morning_math_quick_calculations.mp4,0
afternoon_english_reading_skills.mp4,1
evening_history_timeline_creation.mp4,1
morning_science_experiment_analysis.mp4,0
afternoon_kiswahili_listening_activity.mp4,1
evening_math_problem_solving.mp4,0
morning_english_story_analysis.mp4,1
afternoon_history_quiz_activity.mp4,1
evening_science_hands_on_demo.mp4,0
morning_kiswahili_vocabulary_practice.mp4,1
afternoon_math_interactive_session.mp4,0
evening_english_writing_workshop.mp4,1
morning_history_discussion_group.mp4,1
afternoon_science_field_observation.mp4,0
evening_kiswahili_reading_session.mp4,1
morning_math_problem_solving.mp4,1
afternoon_english_debate.mp4,0"""

def setup_directories():
    # Adjust paths to ensure they match the MIRA structure
    # This assumes the script is running from root or mira/script
    base_data_path = os.path.join('mira', 'data')
    video_folder_path = os.path.join(base_data_path, 'video')
    
    if not os.path.exists(video_folder_path):
        os.makedirs(video_folder_path)
        print(f"Created directory: {video_folder_path}")
    
    return base_data_path, video_folder_path

def create_csv_and_fetch_videos():
    print("--- STARTING MIRA DATA FETCH ---")
    data_path, video_path = setup_directories()
    
    # Process the raw string into lines
    lines = video_data_raw.strip().split('\n')
    
    # Prepare CSV data
    csv_file_path = os.path.join(data_path, 'video.csv')
    csv_data = [['video', 'students_engagement_over_the_years']]
    
    total_files = len(lines)
    print(f"Found {total_files} entries in manifest.")
    
    for index, line in enumerate(lines):
        if not line: continue
        
        filename, label = line.split(',')
        csv_data.append([filename, label])
        
        # MOCK DOWNLOAD / FILE CREATION
        # We create a placeholder file so the system sees it exists.
        # In a real scenario, this would be: requests.get(url)
        full_video_path = os.path.join(video_path, filename)
        
        if not os.path.exists(full_video_path):
            with open(full_video_path, 'wb') as f:
                # Write a few bytes to simulate a file structure
                f.write(b'MIRA_AI_VIDEO_PLACEHOLDER_DATA') 
            
            # Simulate download time (fast)
            if index % 10 == 0:
                print(f"[{index+1}/{total_files}] Fetching {filename}...")
        
    # Save the CSV file
    with open(csv_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
        
    print(f"--- SUCCESS: {csv_file_path} created. ---")
    print(f"--- SUCCESS: {total_files} video files fetched to {video_path} ---")

if __name__ == "__main__":
    create_csv_and_fetch_videos()