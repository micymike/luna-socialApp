FROM python:3.9

# Create a user with a home directory
RUN useradd -m -u 1000 user

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY --chown=user ./requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY --chown=user . /app

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Use the entrypoint script to run the app
ENTRYPOINT ["./entrypoint.sh"]
