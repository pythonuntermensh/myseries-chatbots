package com.myapps.parsermyseries.service;

import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.*;
import com.myapps.parsermyseries.entity.NewSeriesEntity;
import com.myapps.parsermyseries.repository.NewSeriesRepository;
import com.myapps.parsermyseries.util.SeriesAndSeasonsChecker;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.scheduling.annotation.Scheduled;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

@Service
public class NewSeriesService {

    private final String LINK = "http://myseria.pro/series/";

    private final NewSeriesRepository newSeriesRepository;

    @Autowired
    public NewSeriesService(NewSeriesRepository newSeriesRepository) {
        this.newSeriesRepository = newSeriesRepository;
    }

    @Scheduled(fixedDelay = 3, timeUnit = TimeUnit.MINUTES)
    private void parseAndSaveNewSeries() throws IOException, InterruptedException {

        final WebClient webClient = new WebClient();

        webClient.getOptions().setJavaScriptEnabled(false);
        webClient.getOptions().setCssEnabled(false);

        HtmlPage page = webClient.getPage(LINK);

        HtmlElement episodeList = (HtmlElement) page.getElementById("episode_list").getFirstChild();

        List<HtmlElement> newEpisodeList = (List<HtmlElement>) episodeList.getByXPath(".//ul//li");

        for (HtmlElement element : newEpisodeList) {
            HtmlElement info = element.getFirstByXPath(".//div[@class='item']//div[@class='item-serial with-shadow']");

            HtmlElement topInfo = info.getFirstByXPath(".//div[@class='serial-top']");
            HtmlElement bottomInfo = info.getFirstByXPath(".//div[@class='serial-bottom']");

            String name = ((HtmlElement) bottomInfo.getFirstByXPath(".//div[@class='field-title']//a")).getTextContent();
            name = name.substring(0, name.length()-4).strip();
            String link = ((HtmlAnchor) bottomInfo.getFirstByXPath(".//div[@class='field-title']//a")).getHrefAttribute();
            String description = ((HtmlElement) bottomInfo.getFirstByXPath(".//div[@class='field-description']//a")).getTextContent();
            String additional = ((HtmlElement) bottomInfo.getFirstByXPath(".//div[@class='field-title']//a//span")).getTextContent();

            Iterable<DomNode> translationLines = ((HtmlElement) topInfo.getFirstByXPath(".//div[@class='serial-translate']")).getChildren();

            ArrayList<String> translationList = new ArrayList<>();
            for (DomNode node : translationLines) {
                List<HtmlElement> spanList = (List<HtmlElement>) node.getByXPath(".//span");
                for (HtmlElement span : spanList) {
                    translationList.add(span.getFirstChild().getTextContent());
                }
            }
            String pictureStyle = ((HtmlElement) topInfo.getFirstByXPath(".//div[@class='field-img']")).getAttribute("style");
            String pictureUrl = pictureStyle.split("\\(")[1].replace(")", "");

            NewSeriesEntity newSeriesEntity = newSeriesRepository.findByName(name);
            NewSeriesEntity newSeriesEntityUpdated = new NewSeriesEntity(name, description, translationList, link, pictureUrl, additional);
            if (newSeriesEntity != null) {
                if (SeriesAndSeasonsChecker.Compare(newSeriesEntity, newSeriesEntityUpdated) == -1 ) {
                    newSeriesEntity.setDescription(description);
                    newSeriesEntity.setTranslation(translationList);
                    newSeriesEntity.setLink(link);
                    newSeriesEntity.setPictureUrl(pictureUrl);
                    newSeriesEntity.setVKDeprecated(false);
                    newSeriesEntity.setTGDeprecated(false);
                }
                newSeriesRepository.save(newSeriesEntity);
            } else {
                newSeriesRepository.save(newSeriesEntityUpdated);
            }
        }
    }

    public void deprecateData(boolean vk) {
        newSeriesRepository.findAll().forEach((p) -> {
            if (vk) {
                p.setVKDeprecated(true);
            } else {
                p.setTGDeprecated(true);
            }
            newSeriesRepository.save(p);
        });
    }

    public List<NewSeriesEntity> getAllSeries(boolean vk) {
        if (vk) {
            return newSeriesRepository.findAllByVKDeprecated(false);
        }
        return newSeriesRepository.findAllByTGDeprecated(false);
    }
}
