
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class My_crawler {

	static HashSet<String> allLinks = new HashSet<String>();
	static LinkedList<String> queue = new LinkedList<String>();
	static BufferedWriter writer = null;
	static int count = 0;
	
	public static void main (String[] args)
	{
		String url = new String("http://www.ccs.neu.edu");
		String currentUrl;
		int sleep_time = 5000;
		
		try
		{
			writer = new BufferedWriter(new FileWriter("./p2.txt"));
		} catch (IOException e)
		{
			System.out.println(e);
		}

		try
		{
			setupEnv(url+"/robots.txt");
		}
		catch (IOException i)
		{
			System.out.println(i);
		}
		
		try
		{
			setupEnv("http://www.northeastern.edu/robots.txt");
		}
		catch (IOException i)
		{
			System.out.println(i);
		}
		
		allLinks.add(url);
		queue.add(url);
		
		// Implementation of BFS.
		while (!queue.isEmpty() && count < 100)
		{
			currentUrl = queue.pop();
			System.out.println(currentUrl);
			try
			{
				crawl_page(currentUrl);
			}
			catch (IOException i)
			{
				System.out.println(i);
			}
			catch (IllegalArgumentException il)
			{
				System.out.println(il);
			}
			
			// Sleep for 5 secons.
			try
			{
				Thread.sleep(sleep_time);
			} catch (InterruptedException i)
			{
				Thread.currentThread().interrupt();
			}
		}
		
		if (writer != null)
		{
			try
			{
				writer.close();
			} catch (IOException e)
			{
				System.out.println(e);
			}
		}
	}
	
	public static void setupEnv(String rUrl) throws IOException
	{
        Document doc = Jsoup.connect(rUrl).userAgent("*").get();

        String robots = String.valueOf(doc.body());
        String pattern = "Disallow: [a-z/0-9.\\-\\_]*";

        Pattern r = Pattern.compile(pattern);
        Matcher m = r.matcher(robots);


        while(m.find()){
            String URLWithoutDisallow = m.group(0).split("Disallow:")[1].trim();
            allLinks.add(URLWithoutDisallow);
            System.out.println("Found value " + m.group(0).split("Disallow:")[1].trim());

        }

        System.out.println(robots);
	}
	
	// Method to crawl each page.
	public static void crawl_page(String url) throws IOException
	{
		//Connection.Response response = Jsoup.connect(url).userAgent("Mozilla").ignoreContentType(true).execute();
		//Document doc = response.parse();
		System.out.println("Inside Crawler.");
		Document doc = Jsoup.connect(url).userAgent("Mozilla").get();
		
		//if (doc.text().contains("ccs.neu.edu") || doc.text().contains("northeastern.edu"))
		//	System.out.println(url);
		
		writer.write(url+" ");
		
		// Get all links from the page.
		Elements links = doc.select("a[href]");
		
		// Check each link if it needs to be added to output file and queue for crawling.
		for (Element link : links)
		{
			// Convert to Canonical Form.
			String linkUrl = link.attr("href");
			
			if (   !allLinks.contains(linkUrl)
				&& (linkUrl.contains("ccs.neu.edu") || linkUrl.contains(".northeastern.edu"))
				&& count < 100)
			{
				Connection.Response response = null;
				try
				{
					response = Jsoup.connect(linkUrl).userAgent("Mozilla").ignoreContentType(true).execute();
				}
				catch (IOException i)
				{
					System.out.println(i);
				}
				
				if (response.contentType().contains("html"))
				{
					count++;
					System.out.println(linkUrl);
					allLinks.add(linkUrl);
					queue.add(linkUrl);
					
					// Add URL to output file.
					if (linkUrl.contains("html"))
					{
						linkUrl.replaceAll("#*", "");
					}
					writer.write(linkUrl+" ");
				}
				
				if (response.contentType().contains("pdf"))
				{
					// Add to output file.
					writer.write(linkUrl+" ");
				}
				
			}
		}
		
		writer.newLine();
	}
	
}
