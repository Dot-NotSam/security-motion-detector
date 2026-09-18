# Project Statement

## Problem Statement

Manually monitoring a security camera feed for movement is tedious and unreliable over long periods. There is a need for a lightweight, local tool that can automatically flag when motion occurs in a fixed camera view, without depending on heavy deep learning infrastructure or identifying individuals.

## Project Scope

This project covers motion detection only. It compares consecutive video frames to detect meaningful changes and reports them through a desktop dashboard. It does not cover identity recognition, tracking of specific individuals, or license plate reading. The camera is assumed to be fixed (non-moving) for the detection logic to remain valid.

## Target Users

- Computer Vision students learning classical image processing techniques
- Individuals wanting a simple local motion alert tool for a room or entrance
- Anyone needing a basic, explainable motion detection demo without deep learning

## Objectives

- Build a working motion detection pipeline using frame differencing and classical CV operations
- Provide a usable Tkinter interface for starting/stopping monitoring and viewing results
- Log motion events with frame number, timestamp and motion area percentage
- Keep the codebase simple, modular, and runnable on a normal laptop

## High-Level Features

- Webcam and video file input
- Grayscale conversion and Gaussian blur preprocessing
- Frame differencing, thresholding and morphological cleanup
- Contour-based motion region detection with bounding boxes
- Adjustable threshold and minimum motion area
- Real-time status display (MOTION DETECTED / NO MOTION)
- Motion event logging with CSV export

## Expected Outcome

A runnable desktop application that, when pointed at a fixed camera or video file, reliably distinguishes between a stable scene and one with meaningful movement, displays this visually, and keeps a simple record of when motion occurred — without identifying who or what caused it.
