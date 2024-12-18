# Use Python 3.13 as the base image
FROM python:3.11
 
# Set the working directory inside the container
WORKDIR /home/site/wwwroot
 
# Copy all necessary files into the container
COPY . /home/site/wwwroot/
 
# Install Python dependencies from the requirements.txt
RUN pip install --no-cache-dir -r /home/site/wwwroot/requirements.txt
 
# Install Azure Functions SDK for Python
RUN pip install --no-cache-dir azure-functions==1.21.3
 
# Expose port 80 for the function app (default Azure Function port)
EXPOSE 80
 
# Set the entry point to start the Azure Functions runtime
ENTRYPOINT ["func", "host", "start", "--python"]