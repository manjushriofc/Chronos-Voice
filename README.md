# Chronos-Voice
### AI-Powered Audio Forensic Audit System

Chronos-Voice is an audio-forensics project designed to analyze voice recordings for acoustic patterns associated with AI-generated or manipulated speech. It combines audio feature extraction, machine-learning classification, and ONNX-based inference to produce structured analysis results.

## Key Features

- **Audio Analysis:** Extract acoustic features from uploaded voice recordings.
- **Machine Learning:** Use an SVM-based classifier to analyze audio features.
- **ONNX Inference:** Support model inference using the ONNX runtime where implemented.
- **Multilingual Interface:** English, Tamil, and Hindi support, where implemented.
- **Forensic Reporting:** Generate structured analysis reports with trace identifiers and analysis metadata, where implemented.
- **Auditability:** Record relevant analysis metadata to support traceability.

## Technology Stack

Python · Support libraries for audio processing · Scikit-learn · ONNX Runtime

*Update this list to reflect the actual dependencies used in the repository.*

## Important Note

Chronos-Voice provides a model-based assessment, not definitive proof that a voice recording is authentic or manipulated. Predictions may be affected by recording quality, compression, language, speaker characteristics, and differences between training and real-world audio.

## Project Status

See the repository documentation for setup instructions, supported audio formats, evaluation methodology, known limitations, and current development status.
