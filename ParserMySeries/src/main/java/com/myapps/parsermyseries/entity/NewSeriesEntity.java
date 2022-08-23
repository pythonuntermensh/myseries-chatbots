package com.myapps.parsermyseries.entity;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "new_series")
public class NewSeriesEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column
    private String name;

    @Column
    private String description;

    @Column
    private String translation;

    @Column
    private String link;

    @Column
    private String pictureUrl;

    @Column
    private String additional;

    @Column
    private Boolean VKDeprecated;

    @Column
    private Boolean TGDeprecated;

    public NewSeriesEntity() {
    }

    public NewSeriesEntity(String name, String description, ArrayList<String> translation, String link, String pictureUrl, String additional) {
        this.name = name;
        this.description = description;
        this.translation = String.join(";", translation);
        this.link = link;
        this.pictureUrl = pictureUrl;
        this.additional = additional;
        this.VKDeprecated = false;
        this.TGDeprecated = false;
    }

    @Override
    public boolean equals(Object o) {
        if (o == this) {
            return true;
        }

        if (!(o instanceof NewSeriesEntity)) {
            return false;
        }

        NewSeriesEntity c = (NewSeriesEntity) o;

        return this.name.equals(c.getName())
                && this.description.equals(c.getDescription());
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public ArrayList<String> getTranslation() {
        return new ArrayList<>(List.of(translation.split(";")));
    }

    public void setTranslation(ArrayList<String> translation) {
        this.translation = String.join(";", translation);
    }

    public String getLink() {
        return link;
    }

    public void setLink(String link) {
        this.link = link;
    }

    public String getPictureUrl() {
        return pictureUrl;
    }

    public void setPictureUrl(String pictureUrl) {
        this.pictureUrl = pictureUrl;
    }

    public String getAdditional() {
        return additional;
    }

    public void setAdditional(String additional) {
        this.additional = additional;
    }

    public Boolean getVKDeprecated() {
        return VKDeprecated;
    }

    public void setVKDeprecated(Boolean deprecated) {
        this.VKDeprecated = deprecated;
    }

    public Boolean getTGDeprecated() {
        return TGDeprecated;
    }

    public void setTGDeprecated(Boolean deprecated) {
        this.TGDeprecated = deprecated;
    }
}
