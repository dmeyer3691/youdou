package watson;

import java.util.*;
import java.net.*;
import java.io.*;
import json.*;

public class Main {
    
    public static void main(String[] args) throws Exception {
        //String id = "", passwd = "";
        String id = "osu_student1", passwd = "4bfyY9Y4";
        //String question = "What are some classes about video games?";
        //String question = "Who teaches classes about video games?";
        String query = "classes about video games";

        URL watsonURL = new URL("https://watson-wdc01.ihost.com/instance/501/deepqa/v1/question");
        HttpURLConnection conn = (HttpURLConnection) watsonURL.openConnection();
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setRequestProperty("Accept", "application/json");
        conn.setRequestProperty("X-SyncTimeout", "30");

        String auth = new String(Base64.getEncoder().encode((id + ":" + passwd).getBytes()));
        conn.setRequestProperty("Authorization", "Basic " + auth);

        conn.setDoOutput(true);
        conn.getOutputStream().write(("{\"question\" : {\"questionText\":\"" + query + "\"}}").getBytes());
        BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        String inputLine;
        while ((inputLine = in.readLine()) != null) {
            
            /***** initialization *****/
            
            JSONObject object = new JSONObject(inputLine);
            JSONObject object2 = object.optJSONObject("question");
            //System.out.println(object2.toString(5));
            //for (String name : object2.getNames(object2))
            //    System.out.println(">> " + name);
            
            /**********/
            
            System.out.println("\n----------QUERY INFO----------\n");
            
            /***** query info *****/
            
            JSONArray latlist = object2.getJSONArray("latlist");
            JSONArray focuslist = object2.getJSONArray("focuslist");
            JSONArray qclasslist = object2.getJSONArray("qclasslist");
            String questionText = object2.getString("questionText");
            
            //System.out.println(latlist);
            //System.out.println(focuslist);
            //System.out.println(qclasslist);
            System.out.println("QUERY:\t" + questionText);
            for (int i = 0 ; i < latlist.length() ; i++)
                System.out.println("LATLIST:\t" + latlist.getJSONObject(i).get("value"));
            for (int i = 0 ; i < focuslist.length() ; i++)
                System.out.println("FOCUSLIST:\t" + focuslist.getJSONObject(i).get("value"));
            for (int i = 0 ; i < qclasslist.length() ; i++)
                System.out.println("CLASSSLIST:\t" + qclasslist.getJSONObject(i).get("value"));

            /**********/
            
            System.out.println("\n----------ANSWER INFO----------");
            
            /***** answer info *****/
            
            JSONArray evidencelist = object2.getJSONArray("evidencelist");
            JSONArray answers = object2.getJSONArray("answers");
            
            for (int i = 0 ; i < answers.length() ; i++) {
                JSONObject evidence = evidencelist.getJSONObject(i);
                JSONObject answer = answers.getJSONObject(i);
                
                System.out.println("\nTITLE:\t" + evidence.get("title"));
                System.out.println("\tTEXT1:\t" + evidence.get("text"));
                System.out.println("\tTEXT2:\t" + answer.get("text"));
                System.out.println("\tCONF:\t" + answer.get("confidence"));
            }
            
            /**********/
            
            System.out.println("\n----------\n");
            
        }
        in.close();

    }

}
