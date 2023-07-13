import processing.net.*;
import java.util.Arrays;
import java.util.Comparator;

Client client;
ArrayList<PVector> points;
String message;

void setup() {
  size(500, 500);
  client = new Client(this, "localhost", 12345);
  println("Connected to Python");
  pixelDensity(1);
  points = new ArrayList<PVector>();
  for (int i = 0; i < 30; i++) {
    points.add(new PVector(random(width), random(height), random(width)));
  }
  message = "";
}

void draw() {
  while (client.available() > 0) {
    message = client.readString();
    println(message);
  }

  loadPixels();
  for (int x = 0; x < width; x++) {
    for (int y = 0; y < height; y++) {

      float[] distances = new float[points.size()];
      for (int i = 0; i < points.size(); i++) {
        PVector v = points.get(i);
        float z = frameCount % width;
        float d = dist(x, y, z, v.x, v.y, v.z);
        distances[i] = d;
      }
      Arrays.sort(distances);

      float r;
      float g;
      float b;

      // check message and adjust rgb accordingly
      if (message.equals("red")) {
        r = map(distances[0], 0, 150, 0, 255);
        g = map(distances[1], 0, 50, 255, 0);
        b = map(distances[2], 0, 200, 255, 0);
      } else if (message.equals("white")) {
        r = map(distances[0], 0, 150, 200, 255);
        g = map(distances[1], 0, 50, 200, 255);
        b = map(distances[2], 0, 200, 200, 255);
      } else if (message.equals("blue")) {
        r = map(distances[0], 0, 150, 100, 200);
        g = map(distances[1], 0, 50, 130, 200);
        b = map(distances[2], 0, 200, 255, 255);
      } else if (message.equals("yellow")) {
        r = map(distances[0], 0, 150, 0, 255);
        g = map(distances[1], 0, 50, 0, 255);
        b = map(distances[2], 0, 200, 255, 0);
      } else if (message.equals("orange")) {
        r = map(distances[0], 0, 150, 0, 255);
        g = map(distances[1], 0, 50, 0, 140);
        b = map(distances[2], 0, 200, 0, 25);
      } else if (message.equals("magenta")) {
        r = map(distances[0], 0, 150, 0, 255);
        g = map(distances[1], 0, 50, 255, 0);
        b = map(distances[2], 0, 150, 255, 255);
      } else if (message.equals("green")) {
        r = map(distances[0], 0, 150, 255, 0);
        g = map(distances[1], 0, 50, 0, 255);
        b = map(distances[2], 0, 200, 255, 0);
      } else {
        r = map(distances[0], 0, 150, 255, 255);
        g = map(distances[1], 0, 50, 255, 255);
        b = map(distances[2], 0, 200, 255, 255);
      }

      int index = (x + y * width);
      pixels[index] = color(r, g, b);
    }
  }
  updatePixels();
}
