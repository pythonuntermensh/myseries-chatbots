package com.myapps.seriesmanager.service;

import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.DomNode;
import com.gargoylesoftware.htmlunit.html.HtmlAnchor;
import com.gargoylesoftware.htmlunit.html.HtmlElement;
import com.gargoylesoftware.htmlunit.html.HtmlPage;
import com.gargoylesoftware.htmlunit.javascript.host.html.HTMLAnchorElement;
import com.myapps.seriesmanager.entity.SeriesEntity;
import com.myapps.seriesmanager.repository.SeriesRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@Service
public class SeriesService {

    private final SeriesRepository seriesRepository;

    @Autowired
    public SeriesService(SeriesRepository seriesRepository) {
        this.seriesRepository = seriesRepository;
    }

    public void updateSeries() throws IOException {

        seriesRepository.deleteAll();

        final String LINK = "http://myseria.pro/series/";
        final int PAGES_NUM;

        final WebClient webClient = new WebClient();

        webClient.getOptions().setJavaScriptEnabled(false);
        webClient.getOptions().setCssEnabled(false);

        HtmlPage page = webClient.getPage(LINK);

        List<HtmlElement> pagination = new ArrayList<>();
        page.getElementById("pagination").getChildElements().forEach((p) -> pagination.add((HtmlElement) p));

        PAGES_NUM = Integer.parseInt(pagination.get(pagination.size()-2).getTextContent());

        for (int page_number = 1; page_number <= PAGES_NUM; page_number++) {
            page = webClient.getPage(LINK + "page/" + page_number);

            List<HtmlElement> htmlElementToParse = new ArrayList<>();
            page.getElementById("episode_list").getChildElements().forEach((p) -> htmlElementToParse.add((HtmlElement) p));

            for (HtmlElement episodeList : htmlElementToParse) {
                List<HtmlElement> newEpisodeList = (List<HtmlElement>) episodeList.getByXPath(".//ul//li");

                for (HtmlElement element : newEpisodeList) {
                    HtmlElement info = element.getFirstByXPath(".//div[@class='item']//div[@class='item-serial with-shadow']");
                    HtmlElement bottomInfo = info.getFirstByXPath(".//div[@class='serial-bottom']");

                    String name = ((HtmlElement) bottomInfo.getFirstByXPath(".//div[@class='field-title']//a")).getTextContent();
                    name = name.substring(0, name.length() - 4).strip();
                    String additional = ((HtmlElement) bottomInfo.getFirstByXPath(".//div[@class='field-title']//a//span")).getTextContent();

                    if (seriesRepository.findByNameAndAdditional(name, additional) == null) {
                        seriesRepository.save(new SeriesEntity(name, additional));
                    }
                }
            }
        }
    }

    public void testSubAll(Long id, boolean vk) {
        seriesRepository.findAll().forEach((p) -> {
            List<Long> subs = p.getSubscribers(vk);
            if (!subs.contains(id)) {
                subs.add(id);
            }
            p.setSubscribers(subs, vk);
            seriesRepository.save(p);
        });
    }

    public boolean addNewSeries(String name, String additional) {
        if (seriesRepository.findAllByLowRegisterNameAndAdditional(name.toLowerCase(Locale.ROOT), additional).isEmpty()) {
            seriesRepository.save(new SeriesEntity(name, additional));
            return true;
        }
        return false;
    }

    public List<SeriesEntity> getSeries(String[] names) {

        List<SeriesEntity> seriesEntities = new ArrayList<>();
        for (String name : names) {
            List<SeriesEntity> seriesEntity = seriesRepository.findAllByName(name);
            seriesEntities.addAll(seriesEntity);
        }

        return seriesEntities;
    }

    public List<String> getSubscribedSeries(Long id, boolean vk) {
        List<String> subscribedSeries = new ArrayList<>();
        List<SeriesEntity> series = seriesRepository.findAll();

        series.forEach((p) -> {
            if (p.getSubscribers(vk).contains(id)) {
                subscribedSeries.add(p.getName());
            }
        });

        return subscribedSeries.stream().sorted().collect(Collectors.toList());
    }

    public String subscribe(Long id, String name, int num, boolean vk) {
        List<SeriesEntity> seriesEntities = seriesRepository.findAllByLowRegisterName(name.toLowerCase(Locale.ROOT));
        if (num >= seriesEntities.size()) {
            return "Repeat bleat";
        }
        SeriesEntity seriesEntity = seriesEntities.get(num);
        if (seriesEntity != null) {
            List<Long> temp = seriesEntity.getSubscribers(vk);
            if (!temp.contains(id)) {
                temp.add(id);
                seriesEntity.setSubscribers(temp, vk);
                seriesRepository.save(seriesEntity);
                return "Subscribed";
            } else {
                return "Already subscribed";
            }
        } else {
            return "No series";
        }
    }

    public List<SeriesEntity> getAll() {
        return seriesRepository.findAll();
    }

    public String unsubscribe(Long id, String name, int num, boolean vk) {
        List<SeriesEntity> seriesEntities = seriesRepository.findAllByLowRegisterName(name.toLowerCase(Locale.ROOT));
        if (num >= seriesEntities.size()) {
            return "Repeat bleat";
        }
        SeriesEntity seriesEntity = seriesEntities.get(num);
        if (seriesEntity != null) {
            List<Long> temp = seriesEntity.getSubscribers(vk);
            if (temp.contains(id)) {
                temp.remove(id);
                seriesEntity.setSubscribers(temp, vk);
                seriesRepository.save(seriesEntity);
                return "Unsubscribed";
            } else {
                return "Already unsubscribed";
            }
        } else {
            return "No series";
        }
    }

    public List<SeriesEntity> getSeriesWithSameName(String name) {
        return seriesRepository.findAllByLowRegisterName(name.toLowerCase(Locale.ROOT));
    }

    public List<Long> getSubscribers(boolean vk) {
        List<Long> subscribersList = new ArrayList<>();
        seriesRepository.findAll().forEach((p) -> {
            for (Long id : p.getSubscribers(vk)) {
                if (!subscribersList.contains(id)) {
                    subscribersList.add(id);
                }
            }
        });
        return subscribersList;
    }
}
