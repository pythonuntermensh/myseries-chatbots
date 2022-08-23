package com.myapps.parsermyseries.entity;

import javax.persistence.*;

@Entity
public class NoveltySeriesEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column
    private String name;

    @Column
    private String url;

    @Column
    private String pictureUrl;

    @Column
    private boolean VKDeprecated;

    @Column
    private boolean TGDeprecated;

    public NoveltySeriesEntity() {
    }

    public NoveltySeriesEntity(String name, String url, String pictureUrl) {
        this.name = name;
        this.url = url;
        this.pictureUrl = pictureUrl;
        this.VKDeprecated = false;
        this.TGDeprecated = false;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getPictureUrl() {
        return pictureUrl;
    }

    public void setPictureUrl(String pictureUrl) {
        this.pictureUrl = pictureUrl;
    }

    public boolean isVKDeprecated() {
        return VKDeprecated;
    }

    public void setVKDeprecated(boolean VKDeprecated) {
        this.VKDeprecated = VKDeprecated;
    }

    public boolean isTGDeprecated() {
        return TGDeprecated;
    }

    public void setTGDeprecated(boolean TGDeprecated) {
        this.TGDeprecated = TGDeprecated;
    }
}
